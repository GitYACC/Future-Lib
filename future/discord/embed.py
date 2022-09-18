from typing import Generator
import hikari
import lightbulb
from PIL import Image, ImageFont
from rich.console import Console
import time
import sys
import traceback
import re

console = Console()


class BaseEmbed:
    def __init__(self, dim: tuple=(100, 100)):
        with console.status("[green italic]Embedding..."):
            self._init_(dim)

    def _init_(self, dim: tuple):
        time.sleep(2.5)
        if not isinstance(dim, tuple):
            console.print("[red bold]Error: dimensions need to be passed as a tuple")
            return

        



