from enum import Enum
from typing import *

class ComponentType(Enum):
    PANEL = 1
    TEXT = 2
    IMAGE = 3
    HTML = 4


class BaseComponent:
    def __init__(self, name: str, type: ComponentType, **attrs):
        self.name = name
        self.type = type

        # ALL Flags
        self.pos: Tuple[int, int] = attrs.get("position")

        # if self.type == ComponentType.PANEL
        self.repos: Tuple[int, int] = (
            attrs.get("repos") or
            attrs.get("relative-position")
        )
        self.attached_to: self.__class__ = attrs.get("attached-to")
        # self.focus: bool = attrs.get("focus")

        # Partial Flags (excludes Text)
        self.bradius = (
            attrs.get("bradius") or
            attrs.get("border-radius")
        )

        self.bcolor: Tuple[int, int, int] = (
            attrs.get("bcolor") or
            attrs.get("border-color") or
            (0, 0, 0)
        )

        # Panel Flags
        self.bgcolor: Tuple[int, int, int] = (
            attrs.get("bgcolor") or
            attrs.get("background-color") or
            (0, 0, 0)
        )

        self.psize: Tuple[int, int] = (
            attrs.get("psize") or
            attrs.get("panel-size")
        )

        self.children: Dict[str, self.__class__] = {}



        # Text Flags (can be applied into a panel)
        self.text: str = attrs.get("text")
        self.tcolor: Tuple[int, int, int] = (
            attrs.get("tcolor") or
            attrs.get("text-color") or
            (0, 0, 0)
        )

        self.highlight: bool = attrs.get("highlight")
        self.italicize: bool = attrs.get("italicize")
        self.bold: bool = attrs.get("bold")

        # Image Flags
        self.image = (
            attrs.get("image") or
            attrs.get("ipath")
        )

        self.ratio: int = attrs.get("ratio")

        # HTML Flags
        self.html = attrs.get("html")
        self.shtml: str = (
            attrs.get("shtml") or
            attrs.get("string-html")
        )

        self.css = attrs.get("css")
        self.scss: str = (
            attrs.get("scss") or
            attrs.get("string-css")
        )

        self.url = attrs.get("url")

    def __repr__(self):
        return f"BaseComponent [{self.name=}, {self.type=}, {self.pos=}, {self.repos=}, {self.attached_to=}, {self.bradius=}, {self.bcolor=}, {self.bgcolor=}, {self.psize=}, {self.text=}, {self.tcolor=}, {self.image=}, {self.ratio=}, {self.shtml=}, {self.scss=}]"


        

