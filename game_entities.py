from __future__ import annotations

import copy
from typing import Tuple, TypeVar, TYPE_CHECKING
from actions import Action

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

class Entity:
    def __init__(
        self, 
        x: int = 0, 
        y: int = 0, 
        char: str = "?", 
        color: Tuple[int, int, int] = (255,255,255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        health: int = 1,
    ):
        
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.health = health
       
    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        gamemap.entities.add(clone)
        return clone
        
    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy


class Frisbee(Entity):
    def __init__(self, action:Action, damage:int, x:int, y:int, dx:int, dy:int, char: str, color: Tuple[int, int, int]):
        super().__init__(x=x,y=y,char=char,color=color)
        self.dx = dx
        self.dy = dy
        self.action = action
        self.damage = damage
    
   
