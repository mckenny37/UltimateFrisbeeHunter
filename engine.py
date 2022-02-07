from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import MainGameEventHandler

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler
    
class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player
        self.reset = False
                
    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()
        
    
    def refresh_entities(self) -> None:
        for entity in self.game_map.remove_entites:
            self.game_map.entities.remove(entity)
        
        self.game_map.remove_entites.clear()
            

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius = 8
        )
        #If a tile is "visible" it should be added to "explored". |= Or equal operator to make sure to keep old explored tiles and new visible tiles all set to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
       
        console.print(
            x=1,
            y=47,
            string=f"HP: {self.player.component.hp}/{self.player.component.max_hp}"
        )
        context.present(console)
        console.clear()