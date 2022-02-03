from __future__ import annotations

from typing import Iterable, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from game_entities import Entity

class GameMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.entities = set(entities)
        self.remove_entites = set()
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        
        self.visible = np.full((width, height), fill_value=False, order="F") # Tile the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F") # Tile the player has seen before
        
    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

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
            default=tile_types.SHROUD
        ) 
        for ent in self.entities:
            if ent.health <= 0:
                self.remove_entites.add(ent)

        for ent in self.remove_entites:
            self.entities.remove(ent)
        
        self.remove_entites.clear()
          

        for entity in self.entities:
            # Only print entities that are in the FOV
            if self.visible[entity.x,entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)
