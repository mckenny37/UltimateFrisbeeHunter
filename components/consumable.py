from __future__ import annotations
from optparse import Option

from typing import Optional, TYPE_CHECKING

from numpy import isin

import actions
import color
import components.inventory
from components.base_component import BaseComponent
from exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent_entity: Item

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        """Try to return the action for this item."""
        return actions.ItemAction(consumer, self.parent_entity)

    def activate(self, action: actions.ItemAction) -> None:
        """
        Invoke this items ability.

        `action` is the context for this activation
        """
        raise NotImplementedError

    def consume(self) -> None:
        """Remove teh consumed item from its containing inventory."""
        entity = self.parent_entity
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.component.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"You consumer the {self.parent_entity.name}, and recover {amount_recovered} HP!",
                color.health_recovered,
            )
            self.consume()
        else:
            raise Impossible(f"Your health is already full.")
