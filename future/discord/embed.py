from dataclasses import dataclass
from enum import Enum
import hikari
import lightbulb
from typing import Any, Tuple, TextIO, List
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from .component import BaseComponent, ComponentType
from html2image import Html2Image

RGB = Tuple[int, int, int]
RGBA = Tuple[int, int, int, int]

EmbedConfig = {
    "base_color": (55, 57, 62, 1),
    "base_color_transparent": (55, 57, 62, 0),
    "foreground_color": (35, 39, 42),
    "foreground_color_transparent": (35, 39, 42, 0),
    "base_font": "../fonts/Andale Mono.ttf"
}

class EmbedSize(Enum):
    SMALL = 250
    NORMAL = 500
    LARGE = 750


class BaseEmbed:
    def __init__(self, 
        size: EmbedSize = EmbedSize.NORMAL, 
        font: TextIO = EmbedConfig["base_font"], 
        font_size: int = 36,
        fill: RGBA = EmbedConfig["foreground_color"],
        banner: RGB = None,
        lining: bool = False
        # side_banner: RGB = None,
    ):
        # flags
        self._dim = 1000, size.value
        self._font = ImageFont.truetype(font, font_size)
        self._banner = banner
        self._lining = lining
        self._back_fill = EmbedConfig["base_color_transparent"]
        self._front_fill = fill

        self.root = Image.new("RGBA", self.dim, color=self._back_fill)
        self._children = {}
        self.initialize_root()

    @property
    def dim(self): return self._dim

    @property
    def center(self): return self.dim[0] // 2, self.dim[1] // 2

    def center_with(self, component: BaseComponent):
        cen = list(self.center)
        if component.type == ComponentType.TEXT:
            size = self.font.getsize(component.text)
            cen[0] -= size[0] // 2
            cen[1] -= size[1] // 2
        elif component.type == ComponentType.IMAGE:
            bbox = self.ImageProcessing.ratio(
                component, Image.open(component.image)
            ).getbbox()
            cen[0] -= (bbox[2] - bbox[0]) // 2
            cen[1] -= (bbox[3] - bbox[1]) // 2
        elif component.type == ComponentType.PANEL:
            size = component.psize
            cen[0] -= size[0] // 2
            cen[1] -= size[1] // 2
        return tuple(cen)

    @property
    def font(self): return self._font

    @property
    def hasBanner(self): return self._banner is not None

    @property
    def banner(self) -> RGB: return self._banner

    @property
    def hasLining(self): return self._lining == True

    @property
    def backgroundColor(self): return self._back_fill

    @property
    def foregroundColor(self): return self._front_fill

    @property
    def children(self) -> dict: return self._children

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

        if self.hasLining:
            self._init_rounded(draw, pad=1)
        
        if self.hasBanner:
            self._init_rounded(draw, pad=3, fill=self._banner)
            offset_top = 15

        draw.rounded_rectangle(
            (3, offset_top, self.dim[0] - 3, self.dim[1] - 3), 
            radius=25, 
            fill=self._front_fill
        )

    def set_font(self, ttf: str, size: int):
        if not ttf.strip().endswith(".ttf"):
            raise TypeError(f"invalid font file '{ttf}'")

        try:
            self.font = ImageFont.truetype(ttf, size)
        except:
            raise FileNotFoundError(f"could not find ttf file '{ttf}'")

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
        def ratio(command: BaseComponent, im: Image) -> Image:
            if command.ratio:
                div = command.ratio / 100
                w, h = int(im.width * div), int(im.height * div)
                return im.resize((w, h))
            else:
                return im

        @staticmethod
        def border_radius(root, command: BaseComponent, im: Image) -> Image:
            if command.bradius:
                blur_radius = 0
                offset = 4
                back_color = Image.new(im.mode, im.size, root._front_fill)
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
        self._children[command.name] = command
        if command.type == ComponentType.TEXT:
            pos = self._get_pos(command)
                
            renderer.text(
                xy=pos, 
                text=command.text, 
                font=self._font, 
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
            im = Image.new("RGB", command.psize, color=self._front_fill)
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
    
    def save(self, name: str, fp: TextIO = ".") -> str:
        fname = name + (".png" if not name.endswith(".png") else "")
        self.root.save(fname, quality=95)
        return f"{fp}/{fname}"

class Cell:
    component: BaseComponent   = None
    placement: Tuple[int, int] = None
    dimension: Tuple[int, int] = None
    children : List[Any]       = []

    def set(
        self, *,
        component: BaseComponent=None, 
        placement: Tuple[int, int]=None, 
        dimension: Tuple[int, int]=None, 
        children: List[Any]=None
    ):
        if component is not None:
            self.component = component
        
        if placement is not None:
            self.placement = placement

        if dimension is not None:
            self.dimension = dimension

        if children is not None:
            self.children = children

    def add_child(self, cell):
        self.children.append(cell)
        return self

    def __mul__(self, const):
        return [self] * const


class GridEmbed(BaseEmbed):
    def __init__(
        self, 
        size: EmbedSize = EmbedSize.NORMAL, 
        font: TextIO = EmbedConfig["base_font"], 
        font_size: int = 36, 
        fill: RGBA = EmbedConfig["foreground_color"], 
        banner: RGB = None, 
        lining: bool = False,
        grid_dim = (3, 3)
    ):
        super().__init__(size, font, font_size, fill, banner, lining)
        self.grid: Cell = (Cell() * grid_dim[0]) * grid_dim[1]
        

        

        


