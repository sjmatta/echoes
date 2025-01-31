import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
import numpy as np
import soundfile as sf


class AudioProcessor:
    """Handles audio processing, transcription, and diarization."""

    def __init__(
        self,
        config: dict,
        model_manager,
        log_callback: Callable[[str], None],
        progress_callback: Callable[[float, str], None],
    ):
        self.config = config
        self.models = model_manager
        self.write_log = log_callback
        self.update_progress = progress_callback
        self.thread_pool = ThreadPoolExecutor(max_workers=3)

    def process_audio(self, timestamp: str, audio: np.ndarray) -> None:
        """Process and save a recording."""
        self.thread_pool.submit(self._process_audio_task, timestamp, audio)

    def _process_audio_task(self, timestamp: str, audio: np.ndarray) -> None:
        """Task to process and save a recording."""
        try:
            self.write_log("Processing audio data...")
            self.update_progress(0.1, "Preparing audio data...")

            # Save audio file
            output_dir = self.config["output_dir"]
            audio_path = output_dir / f"recording_{timestamp}.flac"
            sf.write(audio_path, audio, 16000, format="FLAC")
            self.write_log(f"Saved audio to {audio_path}")
            self.update_progress(0.2, "Audio saved...")

            # Process audio with models
            future_transcribe = self.thread_pool.submit(
                self._transcribe_audio, audio_path
            )
            future_diarize = self.thread_pool.submit(self._diarize_audio, audio_path)

            segments_list = future_transcribe.result()
            diarization = future_diarize.result()

            # Save results
            self._save_results(segments_list, diarization, timestamp)

        except Exception as e:
            self.write_log(f"\nError processing audio: {str(e)}")
            self.update_progress(1.0, "Error during processing!")
            traceback.print_exc()
        finally:
            # Delete audio file
            if audio_path.exists():
                audio_path.unlink()
                self.write_log(f"Deleted audio file {audio_path}")

    def _transcribe_audio(self, audio_path):
        """Transcribe audio using Whisper model."""
        self.update_progress(0.3, "Transcribing...")
        segments, info = self.models.whisper_model.transcribe(audio_path)
        self.write_log(f"Transcription completed with language: {info.language}")
        self.update_progress(0.6, "Transcription complete...")
        return list(segments)

    def _diarize_audio(self, audio_path):
        """Perform speaker diarization."""
        self.update_progress(0.4, "Diarizing...")
        diarization = self.models.diarization_pipeline(audio_path)
        self.write_log("Diarization completed")
        self.update_progress(0.7, "Diarization complete...")
        return diarization

    def _save_results(self, segments_list, diarization, timestamp):
        """Save combined transcription and diarization results."""
        self.update_progress(0.8, "Combining results...")
        output_path = self.config["output_dir"] / f"transcript_{timestamp}.txt"

        with open(output_path, "w", encoding="utf-8") as f:
            for segment in segments_list:
                # Find speaker for this segment
                start_time = segment.start
                speaker = "Unknown"
                for turn, _, speaker_id in diarization.itertracks(yield_label=True):
                    if turn.start <= start_time <= turn.end:
                        speaker = f"Speaker {speaker_id}"
                        break

                timestamp_str = time.strftime("%H:%M:%S", time.gmtime(segment.start))
                line = f"[{timestamp_str}] {speaker}: " f"{segment.text.strip()}"
                f.write(line + "\n")
                self.write_log(line)

        self.write_log(f"\nSaved complete transcript to {output_path}")
        self.update_progress(1.0, "Processing completed!")
