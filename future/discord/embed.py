from dataclasses import dataclass
from enum import Enum
from queue import Queue
import hikari
import lightbulb
from PIL import Image, ImageFont, ImageDraw
from rich.console import Console
from .component import BaseComponent

console = Console()

@dataclass
class EmbedConfig:
    base_color: tuple = (55, 57, 62)
    foreground_color: tuple = (35, 39, 42)
    text_color: tuple = (163, 180, 191)


class EmbedSize(Enum):
    SMALL = 250
    NORMAL = 500
    LARGE = 750


class BaseEmbed:
    def __init__(self, size: EmbedSize = EmbedSize.NORMAL, font: str = "../fonts/Typomoderno.ttf", font_pixel_size: int = 12):
        with console.status("[green italic]Embedding..."):
           self._init_(size, font, font_pixel_size)

    def _init_(self, size: EmbedSize, font: str, font_pixel_size: int):
        self.dim = (1000, size)
        self.root = Image.new("RGB", self.dim, color=EmbedConfig.base_color)
        self.instructions = Queue(maxsize=-1)
        self.font = ImageFont.truetype(font, font_pixel_size)
        self.initialize_root()

    def initialize_root(self):
        draw = ImageDraw.Draw(self.root)
        draw.rounded_rectangle(
            (3, 3, self.dim[0] - 3, self.dim[1] - 3), 
            radius=25, 
            fill=EmbedConfig.foreground_color
        )

    def set_font(self, ttf: str, size: int):
        if not ttf.endswith(".ttf"):
            raise TypeError(f"invalid font file '{ttf}'")

        try:
            self.font = ImageFont.truetype(ttf, size)
        except:
            raise FileNotFoundError(f"could not find file '{ttf}'")

    def add_component(self, component: BaseComponent):
        self.instructions.put(component)
        return self

    def _process_commands(self):
        while command := self.instructions.get():
            pass
    
    def save(self) -> str:
        self.root.save("test.png")
        return "../env/test.png"
        



