from typing import Callable, List
from datetime import datetime
import numpy as np
from core.audio import AudioDevice
from core.processor import AudioProcessor
from core.models import ModelManager


class AudioController:
    """Controller to handle audio processing logic."""

    def __init__(
        self,
        config: dict,
        write_log: Callable[[str], None],
        update_progress: Callable[[float, str], None],
    ):
        self.config = config
        self.write_log = write_log
        self.update_progress = update_progress

        # Initialize components
        self.model_manager = ModelManager(config, write_log, update_progress)
        self.audio_device = AudioDevice()
        self.audio_processor = AudioProcessor(
            config, self.model_manager, write_log, update_progress
        )

        # State
        self.audio_data: List[np.ndarray] = []
        self.is_recording = False

    def load_models(self):
        """Load ML models."""
        self.model_manager.load_models()

    def start_recording(self, audio_callback: Callable) -> None:
        """Start recording audio."""
        self.is_recording = True
        self.audio_data = []
        self.audio_device.start_recording(audio_callback)

    def stop_recording(self) -> None:
        """Stop recording and process audio."""
        self.is_recording = False
        self.audio_device.stop_recording()
        if self.audio_data:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio = np.concatenate(self.audio_data)
            self.audio_processor.process_audio(timestamp, audio)
            self.audio_data = []
