from enum import auto, Enum


class RenderOrder(Enum):
    # auto() assigns incrementing integer values
    CORPSE = auto()
    ITEM = auto()
    FRISBEE = auto()
    ACTOR = auto()