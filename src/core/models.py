from typing import Callable
from faster_whisper import WhisperModel
from pyannote.audio import Pipeline


class ModelManager:
    """Manages the loading and initialization of ML models."""

    def __init__(
        self,
        config: dict,
        log_callback: Callable[[str], None],
        progress_callback: Callable[[float, str], None],
    ):
        self.config = config
        self.write_log = log_callback
        self.update_progress = progress_callback
        self.whisper_model = None
        self.diarization_pipeline = None

    def load_models(self):
        """Load and initialize Whisper and Pyannote models."""
        try:
            self._load_whisper()
            self._load_pyannote()
            self.write_log("\nAll models loaded successfully! Ready to record.")
            self.update_progress(1.0, "Ready to record")
        except Exception as e:
            error_msg = f"Failed to load models: {str(e)}"
            self.write_log(f"Error: {error_msg}")
            raise RuntimeError(error_msg)

    def _load_whisper(self):
        """Load the Whisper model."""
        self.write_log(
            f"Using Whisper model: {self.config['whisper_model']} on "
            f"{self.config['device']}"
        )
        self.write_log("Downloading Whisper model (this may take a while)...")
        self.update_progress(0.2, "Downloading Whisper model...")

        try:
            self.whisper_model = WhisperModel(
                self.config["whisper_model"],
                device=self.config["device"],
                compute_type=self.config["compute_type"],
                local_files_only=False,
                download_root=None,
            )
            self.write_log("✓ Whisper model loaded successfully")
        except Exception as e:
            self.write_log(f"Error loading Whisper model: {str(e)}")
            raise

    def _load_pyannote(self):
        """Load the Pyannote diarization model."""
        self.write_log("\nInitializing Pyannote diarization model...")
        self.write_log("Note: First run will download several GB of model files...")
        self.update_progress(0.5, "Loading Pyannote model...")

        try:
            self.diarization_pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization", use_auth_token=self.config["hf_token"]
            )
            self.write_log("✓ Pyannote model loaded successfully")
        except Exception as e:
            self.write_log(f"Error loading Pyannote model: {str(e)}")
            raise
