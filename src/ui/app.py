import queue
import threading
from typing import Optional
import numpy as np
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.widgets import Header, Footer, Static, Log
from textual.reactive import reactive
from textual.binding import Binding

from controllers.audio_controller import AudioController
from ui.widgets.audio_meter import AudioMeter
from ui.widgets.processing_progress import ProcessingProgress
from ui.widgets.recording_status import RecordingStatus


class TranscriberApp(App):
    """Main application class for the transcriber UI."""

    CSS = """
    #meter {
        height: 1;
        margin: 1 0;
    }

    #status {
        height: 1;
        margin: 1 0;
    }

    #progress {
        height: 3;
        margin: 1 0;
    }

    #main-container {
        height: 40%;
        border: solid green;
    }

    #log-container {
        height: 60%;
        border: solid yellow;
    }

    .status-text {
        color: blue;
    }
    """

    BINDINGS = [
        Binding("r", "toggle_recording", "Record"),
        Binding("q", "quit", "Quit"),
        Binding("tab", "switch_focus", "Switch Focus"),
    ]

    # Reactive properties for state management
    is_recording = reactive(False)

    def __init__(self, config: dict):
        """Initialize the application with configuration."""
        super().__init__()
        self.config = config
        self.audio_queue = queue.Queue()
        self.controller = AudioController(config, self.write_log, self.update_progress)

        # Widget references
        self._log: Optional[Log] = None
        self._meter: Optional[AudioMeter] = None
        self._status: Optional[RecordingStatus] = None
        self._progress: Optional[ProcessingProgress] = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        with Vertical(id="main-container"):
            yield AudioMeter()
            yield RecordingStatus()
            yield ProcessingProgress(id="progress")
            yield Static("Press [R] to start/stop recording", classes="status-text")

        with ScrollableContainer(id="log-container"):
            yield Log()

        yield Footer()

    async def on_mount(self) -> None:
        """Initialize the app after mounting."""
        # Get widget references
        self._log = self.query_one(Log)
        self._meter = self.query_one(AudioMeter)
        self._status = self.query_one(RecordingStatus)
        self._progress = self.query_one(ProcessingProgress)

        # Show initial status
        self.write_log("Starting Transcriber App...")
        self.write_log(f"Output directory: {self.config['output_dir']}")
        self.update_progress(0.0, "Loading models...")

        # Start model loading in the background
        def load_models_worker():
            try:
                self.controller.load_models()
            except Exception as e:
                self.write_log(f"Error loading models: {str(e)}")
                self.exit(str(e))

        self.write_log("Starting model initialization...")
        worker = threading.Thread(target=load_models_worker)
        worker.daemon = True
        worker.start()

    def update_progress(self, progress: float, status: str) -> None:
        """Update the progress bar and status message."""
        if self._progress:
            self._progress.progress = progress
            self._progress.status = status
            self._progress.refresh()

    def write_log(self, message: str) -> None:
        """Write a message to the log widget."""
        if self._log is not None:
            self._log.write(f"\n{message}")

    def audio_callback(self, indata, frames, time, status):
        """Handle audio data from the input stream."""
        if status:
            self.write_log(f"Audio callback status: {str(status)}")

        # Calculate audio level for meter
        audio_level = np.sqrt(np.mean(indata**2))

        # Store audio data if recording
        if self.controller.is_recording:
            self.controller.audio_data.append(indata.copy())

        # Update audio meter
        if self._meter:
            self._meter.level = min(audio_level * 5, 1.0)

    def action_toggle_recording(self) -> None:
        """Toggle recording state on/off."""
        if self.controller.is_recording:
            self.controller.stop_recording()
            self.write_log("Recording stopped")
        else:
            self.controller.start_recording(self.audio_callback)
            self.write_log("Recording started")
            self.update_progress(0.0, "Recording in progress...")

        if self._status:
            self._status.recording = self.controller.is_recording

    def action_switch_focus(self) -> None:
        """Switch focus between main and log containers."""
        if self.focused == self.query_one("#main-container"):
            self.query_one("#log-container").focus()
        else:
            self.query_one("#main-container").focus()
