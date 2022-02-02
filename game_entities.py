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
    def __init__(self, action:Action, damage:int, x:int, y:int, dx:int, dy:int, char: str, color: Tuple[int, int, int]):
        super().__init__(x=x,y=y,char=char,color=color)
        self.dx = dx
        self.dy = dy
        self.action = action
        self.damage = damage
    
class Boss(Entity):
    def __init__(self, health:int, x:int, y:int, char: str, color: Tuple[int, int, int]):
        super().__init__(x=x,y=y,char=char,color=color)
        self.health = health
    

        
    
