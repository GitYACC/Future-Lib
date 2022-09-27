from enum import Enum
from typing import *

class ComponentType(Enum):
    PANEL = 1
    TEXT = 2
    IMAGE = 3


class BaseComponent:
    def __init__(self, name: str, type: ComponentType, **attrs):
        self.name = name
        self.type = type

        # ALL Flags
        self.pos: tuple = attrs.get("position")
        # self.focus: bool = attrs.get("focus")

        # Partial Flags (excludes Text)
        self.bradius: int = (
            attrs.get("bradius") or
            attrs.get("border-radius")
        )

        self.border: bool = attrs.get("border")
        self.bcolor: hex = (
            attrs.get("bcolor") or
            attrs.get("border-color")
        )

        # Panel Flags
        self.bgcolor: hex = (
            attrs.get("bgcolor") or
            attrs.get("background-color")
        )


        # Text Flags
        self.text: str = attrs.get("text")
        self.tcolor: tuple = (
            attrs.get("tcolor") or
            attrs.get("text-color")
        )

        self.highlight: hex = attrs.get("highlight")
        self.italicize: slice = attrs.get("italicize")
        self.bold: slice = attrs.get("bold")

        # Image Flags
        self.image: str = (
            attrs.get("image") or
            attrs.get("ipath")
        )

        self.ratio: int = attrs.get("ratio")


        

