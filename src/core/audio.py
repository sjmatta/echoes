from typing import Optional, Callable
import sounddevice as sd


class AudioDevice:
    """Handles audio device interaction and recording."""

    def __init__(self):
        self._stream: Optional[sd.InputStream] = None

    def start_recording(self, callback: Callable) -> None:
        """Start recording audio using the provided callback."""
        try:
            self._stream = sd.InputStream(
                callback=callback, channels=1, samplerate=16000
            )
            self._stream.start()
        except Exception as e:
            raise RuntimeError(f"Error starting recording: {str(e)}") from e

    def stop_recording(self) -> None:
        """Stop the current recording."""
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
