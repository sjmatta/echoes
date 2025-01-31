from textual.reactive import reactive
from textual.widgets import Static


class RecordingStatus(Static):
    """Widget showing recording status with animation"""

    recording = reactive(False)
    frames = ["⚫", "⚪"]

    def on_mount(self) -> None:
        self.frame_index = 0
        self.set_interval(0.5, self.animate)

    def animate(self) -> None:
        if self.recording:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.refresh()

    def render(self) -> str:
        if not self.recording:
            return "Stopped ⚫"
        return f"Recording {self.frames[self.frame_index]}"
