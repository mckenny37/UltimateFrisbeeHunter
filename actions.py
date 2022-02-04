from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from game_entities import Entity

class Action:
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objectsa needed to determine its scope
        
        `self.engine` is the scope this action is being performed in.

        `self.entitiy` is the object performing the action.

        This method must be overidden by Action subclasses.
        """
        raise NotImplementedError 

class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class WaitAction(Action):
    def perform(self) -> None:
        pass

class ActionWithDirection(Action):
    def __init__(self, entity: Entity, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy
        
    @property
    def dest_xy(self) -> Tuple[int,int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination"""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)
    
    def perform(self) -> None:
        raise NotImplementedError()
    
class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.blocking_entity
        if not target:
            return # No entity to attack.

        print(f"You kick the {target.name}, much to its annoyance!")

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return # Destination out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x,dest_y]:
            return # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return # Destination is blocked by an entity.

        self.entity.move(self.dx, self.dy)
        
class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.blocking_entity:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
        
class ProjectileAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y) or not self.engine.game_map.tiles["walkable"][dest_x,dest_y]:
            self.engine.game_map.remove_entites.add(self.entity)
            return # Destination out of bounds, so end projectile

        #Check if there is an enemy in destination, if so then we damage the enemy and remove projectile
        entity_detected = self.blocking_entity
        if entity_detected != None:
            entity_detected .health -= entity_detected .damage
            self.engine.game_map.remove_entites.add(self.entity)


        self.entity.move(self.dx, self.dy)

class ShootAction(ActionWithDirection):
    def perform(self) -> None:
        from game_entities import Frisbee
        projectile = Frisbee(damage=1, x=self.entity.x, y=self.entity.y, dx=self.dx, dy=self.dy, char="O", color=[56,0,56])
        projectile.place(self.dx, self.dy, self.engine.game_map)
        self.engine.game_map.entities.add(projectile)