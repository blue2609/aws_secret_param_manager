from rich.console import Console
from rich.style import Style
from rich.text import Text
from rich import box
from rich.panel import Panel

class Heading:
    def __init__(self, text: str, foreground: str = "white"):
        self.text = text
        self.foreground = foreground

    def __rich_console__(self, console: Console, options: "ConsoleOptions"):
        styled_text = Text(
            self.text,
            style=Style(color=self.foreground, bold=True)
        )
        return [Panel(styled_text, box=box.ROUNDED)]
