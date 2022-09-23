from dataclasses import dataclass
from enum import Enum
from queue import Queue
import hikari
import lightbulb
import typing
from PIL import Image, ImageFont, ImageDraw
from .component import BaseComponent, ComponentType

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
    def __init__(self, size: EmbedSize = EmbedSize.NORMAL, font: typing.TextIO = "../fonts/Andale Mono.ttf", font_pixel_size: int = 12):
        self.dim = (1000, size.value)
        self.root = Image.new("RGB", self.dim, color=EmbedConfig.base_color)
        self.instructions: typing.List[BaseComponent] = Queue(maxsize=-1)
        self.font = ImageFont.truetype(font, font_pixel_size)
        self.children = {}
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
        renderer = ImageDraw.Draw(self.root)
        while command := self.instructions.get():
            if command.type == ComponentType.TEXT:
                self.children[command.name] = command
                renderer.multiline_textbbox(command.pos, command.text, font=self.font)
                break
        

    
    def save(self, name: str, fp: typing.TextIO) -> str:
        self._process_commands()
        fname = name + (".png" if not name.endswith(".png") else "")
        self.root.save(fname)
        return f"{fp}/{fname}"
        



