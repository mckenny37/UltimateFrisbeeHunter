from components.ai import HostileEnemy, Projectile
from components import consumable
from components.fighter import Fighter
from components.frisbee import Frisbee
from components.inventory import Inventory
from entity import Actor, Item

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    component=Fighter(hp=30, defense=2, power=5),
    inventory=Inventory(capacity=26),
)

frisbee = Actor(
    char="o",
    color=(75, 0, 130),
    name="Frisbee",
    blocks_movment=False,
    ai_cls=Projectile,
    component=Frisbee(power=player.component.power, dx=0, dy=-1),
)

orc = Actor(
    char="O",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    component=Fighter(hp=10, defense=0, power=3)
)
troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    component=Fighter(hp=16, defense=1, power=4)
)
boss = Actor(
    char="B",
    color=(255, 255, 255),
    name="Boss",
    ai_cls=HostileEnemy,
    component=Fighter(hp=30, defense=2, power=5)
)

health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(
        damage=20, maximum_range=5),
)
