from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple

import numpy as np # type: ignore
import tcod

from actions import Action, AttackAction, MovementAction, WaitAction
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor
    

class BaseAI(Action, BaseComponent):
    entity: Actor

    def perform(self) -> None:
        raise NotImplementedError

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int,int]]:
        """
        Compute and return a path to the target position.
        If there is no valid path then returns an empty list.
        """
        
        # Copy the walkable array.
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # Check that an entity blocks movement and the cost isn't zero (blocking).
            if entity.blocks_movement and cost[entity.x, entity.y]:
                """
                A lower number means more enemies will crowd behind each other in
                hallways. A higher number means enemmies will take longer path in 
                order to surround the player.
                """
                cost[entity.x,entity.y] += 10
                
        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y)) # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int,int]].
        return [(index[0], index[1]) for index in path]

class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int,int]] =[]

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy)) # Cheyshev distance.

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return AttackAction(self.entity, dx, dy).perform()

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y).perform()

        return WaitAction(self.entity).perform()

class Projectile(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        dest_x = self.entity.x + self.entity.component.dx
        dest_y = self.entity.y + self.entity.component.dy

        if self.engine.game_map.get_actor_at_location(dest_x,dest_y):
            #Frisbee found target so attack and then remove frisbee
            self.engine.game_map.remove_entites.add(self.entity)
            return AttackAction(self.entity, self.entity.component.dx, self.entity.component.dy).perform()
        elif not self.engine.game_map.in_bounds(dest_x, dest_y) or not self.engine.game_map.tiles["walkable"][dest_x,dest_y]:
            self.engine.game_map.remove_entites.add(self.entity)
            return # Destination out of bounds, so end projectile
        else:
            return MovementAction(self.entity, self.entity.component.dx, self.entity.component.dy).perform()
