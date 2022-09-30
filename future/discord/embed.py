from dataclasses import dataclass
from enum import Enum
from queue import Queue
import hikari
import lightbulb
import typing
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from .component import BaseComponent, ComponentType

RGB = typing.Tuple[int, int, int]
RGBA = typing.Tuple[int, int, int, int]

@dataclass
class EmbedConfig:
    base_color: RGBA = (55, 57, 62, 1)
    base_color_transparent: RGBA = (55, 57, 62, 0)
    foreground_color: RGB = (35, 39, 42)


class EmbedSize(Enum):
    SMALL = 250
    NORMAL = 500
    LARGE = 750


class BaseEmbed:
    def __init__(self, 
        size: EmbedSize = EmbedSize.NORMAL, 
        font: typing.TextIO = "../fonts/Andale Mono.ttf", 
        font_size: int = 36,
        fill: RGBA = EmbedConfig.foreground_color,
        banner: RGB = None,
        lining: bool = False
        # side_banner: RGB = None,
    ):
        # flags
        self.dim = (1000, size.value)
        self.font = ImageFont.truetype(font, font_size)
        self.banner = banner
        self.lining = lining
        self.back_fill = EmbedConfig.base_color_transparent
        self.front_fill = fill

        self.root = Image.new("RGBA", self.dim, color=self.back_fill)
        self.instructions = Queue(maxsize=-1)
        self.children = {}
        self.initialize_root()

    def __rounded(self, render, pad=3, fill=(0, 0, 0)):
        render.rounded_rectangle(
            (pad, pad, self.dim[0] - pad, self.dim[1] - pad),
            radius=25,
            fill=fill
        )

    def initialize_root(self):
        draw = ImageDraw.Draw(self.root)
        offset_top = 3

        if self.lining:
            self.__rounded(draw, pad=1)
        
        if self.banner:
            self.__rounded(draw, pad=3, fill=self.banner)
            offset_top = 15

        draw.rounded_rectangle(
            (3, offset_top, self.dim[0] - 3, self.dim[1] - 3), 
            radius=25, 
            fill=self.front_fill
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
        self.instructions.put(ENDQ:=1)
        renderer = ImageDraw.Draw(self.root)
        while (command := self.instructions.get()) != ENDQ:
            self.children[command.name] = command
            if command.type == ComponentType.TEXT:
                renderer.text(
                    xy=command.pos, 
                    text=command.text, 
                    font=self.font, 
                    fill=command.tcolor,
                    features="ital" if command.italicize else None
                )
            elif command.type == ComponentType.IMAGE:
                im = Image.open(command.image)
                if command.ratio:
                    div = command.ratio / 100
                    w, h = int(im.width * div), int(im.height * div)
                    im = im.resize((w, h))
                
                if command.bradius:
                    blur_radius = 0
                    offset = 4
                    back_color = Image.new(im.mode, im.size, self.front_fill)
                    offset = blur_radius * 2 + offset
                    mask = Image.new("L", im.size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((offset, offset, im.size[0] - offset, im.size[1] - offset), fill=255)
                    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

                    ims_round = Image.composite(im, back_color, mask)
                    im = ims_round
                
                self.root.paste(im, command.pos)
            elif command.type == ComponentType.PANEL:
                #self.root.paste(Image.open(command.image), command.pos)
                pass
        

    
    def save(self, name: str, fp: typing.TextIO) -> str:
        self._process_commands()
        fname = name + (".png" if not name.endswith(".png") else "")
        self.root.save(fname, quality=95)
        return f"{fp}/{fname}"
        



