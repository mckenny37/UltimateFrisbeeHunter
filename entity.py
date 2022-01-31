from numpy import block
from typing import Tuple
from actions import Action


class Entity:
    def __init__(self, x:int, y:int, char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
       
    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy


class Frisbee(Entity):
    def __init__(self, action:Action, x:int, y:int, dx:int, dy:int, char: str, color: Tuple[int, int, int]):
        super().__init__()
        print("here")
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.char = char
        self.color = color
        self.action = action
        
    def move(self) -> None:
        # Move the entity by a given amount
        self.x += self.dx
        self.y += self.dy

