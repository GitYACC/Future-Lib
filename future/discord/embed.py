from dataclasses import dataclass
from enum import Enum
from queue import Queue
import hikari
import lightbulb
import typing
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from .component import BaseComponent, ComponentType
from html2image import Html2Image

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
        self.children = {}
        self.initialize_root()

    def _init_rounded(self, render, pad=3, fill=(0, 0, 0), radius=25):
        render.rounded_rectangle(
            (pad, pad, self.dim[0] - pad, self.dim[1] - pad),
            radius=radius,
            fill=fill
        )

    def _panel_rounded(self, render, pad=3, dim=None, fill=(255, 255, 255), radius=25):
        render.rounded_rectangle(
            (pad, pad, dim[0] - pad, dim[1] - pad),
            radius=radius,
            fill=fill
        )

    def initialize_root(self):
        draw = ImageDraw.Draw(self.root)
        offset_top = 3

        if self.lining:
            self._init_rounded(draw, pad=1)
        
        if self.banner:
            self._init_rounded(draw, pad=3, fill=self.banner)
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

    def _get_pos(self, command: BaseComponent):
        if command.repos and command.attached_to:
            t1 = command.attached_to.pos
            t2 = command.repos
            return (t1[0] + t2[0], t1[1] + t2[1])
        return command.pos

    def add_component(self, component: BaseComponent):
        self._process_command(component)
        return self

    class ImageProcessing:
        @staticmethod
        def ratio(command: BaseComponent, im: Image, root = None):
            if command.ratio:
                div = command.ratio / 100
                w, h = int(im.width * div), int(im.height * div)
                return im.resize((w, h))
            else:
                return im

        @staticmethod
        def border_radius(root, command: BaseComponent, im: Image):
            if command.bradius:
                blur_radius = 0
                offset = 4
                back_color = Image.new(im.mode, im.size, root.front_fill)
                offset = blur_radius * 2 + offset
                mask = Image.new("L", im.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((offset, offset, im.size[0] - offset, im.size[1] - offset), fill=255)
                mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

                ims_round = Image.composite(im, back_color, mask)
                return ims_round
            else:
                return im

    def _process_command(self, command: BaseComponent):
        renderer = ImageDraw.Draw(self.root)
        self.children[command.name] = command
        if command.type == ComponentType.TEXT:
            pos = self._get_pos(command)
                
            renderer.text(
                xy=pos, 
                text=command.text, 
                font=self.font, 
                fill=command.tcolor,
                features="ital" if command.italicize else None
            )
        elif command.type == ComponentType.IMAGE:
            pos = self._get_pos(command)
            im = Image.open(command.image)
            im = self.ImageProcessing.ratio(command, im)
            im = self.ImageProcessing.border_radius(self, command, im)
            self.root.paste(im, pos)
        elif command.type == ComponentType.PANEL:
            pos = self._get_pos(command)
            im = Image.new("RGB", command.psize, color=self.front_fill)
            render = ImageDraw.Draw(im)
            self._panel_rounded(render, dim=im.size, fill=command.bgcolor)
            self.root.paste(im, pos)
        elif command.type == ComponentType.HTML:
            pos = self._get_pos(command)

            hti = Html2Image()
            if command.url:
                hti.screenshot(url=command.url)
            elif command.shtml or command.scss:
                hti.screenshot(
                    html_str=command.shtml or [], 
                    css_str=command.scss or []
                )
            elif command.html or command.css:
                hti.screenshot(
                    html_file=command.html or [],
                    css_file=command.css or []
                )

            im = Image.open(f"screenshot.png").crop((0, 0, self.dim[0], self.dim[1]))

            im = self.ImageProcessing.ratio(command, im)
            self.root.paste(im, pos)
    
    def save(self, name: str, fp: typing.TextIO) -> str:
        fname = name + (".png" if not name.endswith(".png") else "")
        self.root.save(fname, quality=95)
        return f"{fp}/{fname}"
        



