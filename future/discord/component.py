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
        self.pos = self._enforce_type(attrs.get("position"), tuple, "position")

        # if self.type == ComponentType.PANEL
        self.repos = self._enforce_type((
            attrs.get("repos") or
            attrs.get("relative_position")
        ), tuple, "relative-position")
        # self.focus: bool = attrs.get("focus")

        # Partial Flags (excludes Text)
        self.bradius = self._enforce_type((
            attrs.get("bradius") or
            attrs.get("border-radius")
        ), int, "border-radius")

        self.bcolor = self._enforce_type((
            attrs.get("bcolor") or
            attrs.get("border-color") or
            (0, 0, 0)
        ), tuple, "border-color")

        # Panel Flags
        self.bgcolor = self._enforce_type((
            attrs.get("bgcolor") or
            attrs.get("background-color") or
            (0, 0, 0)
        ), tuple, "background-color")

        self.psize = self._enforce_type((
            attrs.get("psize") or
            attrs.get("panel-size")
        ), tuple, "panel-size")


        # Text Flags (can be applied into a panel)
        self.text = self._enforce_type(attrs.get("text"), str, "text")
        self.tcolor = self._enforce_type((
            attrs.get("tcolor") or
            attrs.get("text-color") or
            (0, 0, 0)
        ), tuple, "text-color")

        self.highlight = self._enforce_type(attrs.get("highlight"), tuple, "highlight")
        self.italicize = self._enforce_type(attrs.get("italicize"), bool, "italicize")
        self.bold = self._enforce_type(attrs.get("bold"), bool, "bold")

        # Image Flags
        self.image = self._enforce_type((
            attrs.get("image") or
            attrs.get("ipath")
        ), str, "image")

        self.ratio = self._enforce_type(attrs.get("ratio"), int, "ratio")

    def _enforce_type(self, attr, type, attr_name):
        if not attr:
            return attr

        if not isinstance(attr, type):
            raise TypeError(f"'{attr_name}' requires a {type}")

        return attr


        

