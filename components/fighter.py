from __future__ import annotations
from subprocess import DETACHED_PROCESS

from typing import TYPE_CHECKING

import color
from components.actor_component import ActorComponent
from input_handlers import GameOverEventHandler
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(ActorComponent):
    parent_entity: Actor

    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent_entity.ai:
            self.die()

    def die(self) -> None:
        if self.engine.player is self.parent_entity:
            death_message = "You died!"
            death_message_color = color.player_die
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"{self.parent_entity.name} is dead!"
            death_message_color = color.enemy_die

        self.parent_entity.char = "%"
        self.parent_entity.color = (191, 0, 0)
        self.parent_entity.blocks_movement = False
        self.parent_entity.ai = None
        self.parent_entity.name = f"remains of {self.parent_entity.name}"
        self.parent_entity.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = min(self.max_hp, self.hp + amount)

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
