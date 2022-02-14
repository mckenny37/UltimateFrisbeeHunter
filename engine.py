from __future__ import annotations
from logging import exception

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler


class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def refresh_entities(self) -> None:
        for entity in self.game_map.remove_entites:
            self.game_map.entities.remove(entity)

        self.game_map.remove_entites.clear()

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8
        )
        # If a tile is "visible" it should be added to "explored". |= Or equal operator to make sure to keep old explored tiles and new visible tiles all set to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21,
                                y=45, width=40, height=5)

        render_bar(
            console=console,
            current_value=self.player.component.hp,
            maximum_value=self.player.component.max_hp,
            total_width=20,
        )

        render_names_at_mouse_location(
            console=console, x=21, y=44, engine=self)
