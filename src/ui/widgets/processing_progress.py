from textual.reactive import reactive
from textual.widgets import Static


class ProcessingProgress(Static):
    """Widget for showing processing progress"""

    progress = reactive(0.0)
    status = reactive("")

    def render(self) -> str:
        width = self.size.width - 2
        filled_width = int(self.progress * width)
        bar = "█" * filled_width + "░" * (width - filled_width)
        percentage = int(self.progress * 100)
        return f"{self.status}\n[blue]│{bar}│ {percentage}%[/]"
