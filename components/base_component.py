from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_map import GameMap


class BaseComponent:
    parent_entity: Entity  # Owning entity instance.

    @property
    def gamemap(self) -> GameMap:
        return self.parent_entity.gamemap

    @property
    def engine(self) -> Engine:
        return self.gamemap.engine
