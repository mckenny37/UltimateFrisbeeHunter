from __future__ import annotations
from tkinter import Y

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from game_entities import Entity

class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objectsa needed to determine its scope
        
        `engine` is the scope this action is being performed in.

        `entitiy` is the object performing the action.

        This method must be overidden by Action subclasses.
        """
        raise NotImplementedError 

class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy
        
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()
    
class MeleeAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)
        if not target:
            return # No entity to attack.

        print(f"You kick the {target.name}, much to its annoyance!")

class MovementAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return # Destination out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x,dest_y]:
            return # Destination is blocked by a tile.
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return # Destination is blocked by an entity.

        entity.move(self.dx, self.dy)
        
class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)
        
class ProjectileAction(Action):
    def __init__(self):
        super().__init__()

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + entity.dx
        dest_y = entity.y + entity.dy

        if not engine.game_map.in_bounds(dest_x, dest_y) or not engine.game_map.tiles["walkable"][dest_x,dest_y]:
            engine.game_map.remove_entites.add(entity)
            return # Destination out of bounds, so end projectile

        #Check if there is an enemy in destination, if so then we damage the enemy and remove projectile
        for entities in engine.game_map.entities:
            if [entities.x, entities.y] == [dest_x, dest_y]:
                entities.health -= entity.damage
                engine.game_map.remove_entites.add(entity)


        entity.move(entity.dx, entity.dy)

class ShootAction(Action):
    def __init__(self):
        super().__init__()

    def perform(self, engine: Engine, entity: Entity) -> None:
        from game_entities import Frisbee
        dx = 0
        dy = -1
        projectile = Frisbee(action=ProjectileAction(), damage=1, x=entity.x, y=entity.y, dx=dx, dy=dy, char="O", color=[128,0,128])
        engine.game_map.entities.add(projectile)