from __future__ import annotations
from html.entities import entitydefs

from typing import Iterable, Iterator, Optional, TYPE_CHECKING
from xml.sax.handler import property_declaration_handler

import numpy as np  # type: ignore
from tcod.console import Console

from game_entities import Actor
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from game_entities import Entity

class GameMap:
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
        ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.remove_entites = set()
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        
        self.visible = np.full(
            (width, height), fill_value=False, order="F"
            ) # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        ) # Tile the player has seen before
        
    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    def get_blocking_entity_at_location(
        self, location_x: int, location_y: int
        ) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None   

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        
        return None
        
    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Render the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, thend raw it with the "dark" colors.
        Otherwise, teh default is "SHROUD".
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        ) 

        for entity in self.entities:
            # Only print entities that are in the FOV
            if self.visible[entity.x,entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)
