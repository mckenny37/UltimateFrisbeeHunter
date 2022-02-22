from __future__ import annotations

import random
from typing import List, Optional, Tuple, TYPE_CHECKING

import numpy as np  # type: ignore
import tcod

from actions import Action, AttackAction, BumpAction, MovementAction, WaitAction

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action):

    def perform(self) -> None:
        raise NotImplementedError

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
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
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[
            1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int,int]].
        return [(index[0], index[1]) for index in path]


class ConfusedEnemy(BaseAI):
    """
    A confused enemy will stubmle around aimlessly for a given number of turns, then revert back to it's previous AI.
    If an actor occupies a tile it is randomly moving into, it will attack.
    """

    def __init__(
        self, entity: Actor, previous_ai: Optional[BaseAI], turns_remaining: int
    ) -> None:
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self) -> None:
        # Rever the AI back to the original state if the effect has run its course.
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(
                f"The {self.entity.name} is no longer confused."
            )
            self.entity.ai = self.previous_ai
        else:
            # Pick a random direction
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
                ]
            )

            self.turns_remaining -= 1

            # The actor will either try to move or attack in the chosen random direction.
            # It's possible the actor will just bump into the wall, wasting a turn.
            return BumpAction(self.entity, direction_x, direction_y).perform()


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Cheyshev distance.

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

        if self.engine.game_map.get_actor_at_location(dest_x, dest_y):
            # Frisbee found target so attack and then remove frisbee
            action = AttackAction(
                self.entity, self.entity.component.dx, self.entity.component.dy).perform()
            self.engine.game_map.entities.remove(self.entity)
            return action
        elif not self.engine.game_map.in_bounds(dest_x, dest_y) or not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            self.engine.game_map.entities.remove(self.entity)
            return  # Destination out of bounds, so end projectile
        else:
            return MovementAction(self.entity, self.entity.component.dx, self.entity.component.dy).perform()
