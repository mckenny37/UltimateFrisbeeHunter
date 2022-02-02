from html import entities
from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from game_entities import Boss, Entity, Frisbee
from game_map import GameMap
from input_handlers import EventHandler

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.remove_entites: Set[Entity] = set()
        self.reset = False
        
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            
            action.perform(self, self.player)
            
        for ent in self.entities:
            if isinstance(ent, Frisbee):
                ent.action.perform(self, ent)
            if isinstance(ent, Boss):
                if ent.health <= 0:
                    self.remove_entites.add(ent)
                    self.reset = True
                    self.remove_entites.add(ent)
        for ent in self.remove_entites:
            self.entities.remove(ent)
        
        self.remove_entites.clear()

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        
        for entity in self.entities:
            #print (entity.char)
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)
        console.clear()