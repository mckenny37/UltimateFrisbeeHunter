from __future__ import annotations

from typing import TYPE_CHECKING

from components.actor_component import ActorComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Frisbee(ActorComponent):
    parent_entity: Actor

    def __init__(self, dx: int, dy: int, power: int):
        self.power = power
        self.dx = dx
        self.dy = dy
        self.blocks_movement = False
