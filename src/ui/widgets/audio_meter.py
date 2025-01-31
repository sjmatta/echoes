from textual.reactive import reactive
from textual.widgets import Static


class AudioMeter(Static):
    """A custom widget for displaying audio levels"""

    level = reactive(0.0)

    def __init__(self):
        super().__init__()
        self.gradient = ["green", "green", "yellow", "yellow", "red"]

    def compute_level_colors(self, value: float) -> list[str]:
        segments = len(self.gradient)
        index = min(int(value * segments), segments - 1)
        return self.gradient[: index + 1]

    def render(self) -> str:
        width = self.size.width - 2
        level_width = int(self.level * width)
        colors = self.compute_level_colors(self.level)

        bar = ""
        remaining_width = level_width
        segment_width = width // len(self.gradient)

        for color in colors:
            segment = min(remaining_width, segment_width)
            if segment <= 0:
                break
            bar += f"[{color}]{'█' * segment}[/]"
            remaining_width -= segment

        padding = " " * (width - len(bar))
        return f"│{bar}{padding}│"
