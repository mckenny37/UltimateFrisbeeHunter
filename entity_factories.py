from components.ai import HostileEnemy, Projectile
from components.fighter import Fighter
from components.frisbee import Frisbee
from entity import Actor

player = Actor(
    char="@",
    color=(255,255,255), 
    name="Player", 
    ai_cls=HostileEnemy, 
    component = Fighter(hp=30, defense=2, power=5)
)
frisbee = Actor(
    char="o",
    color=(75,0,130),
    name="Frisbee",
    ai_cls=Projectile,
    component=Frisbee(power=player.component.power, dx=0, dy=-1),
)
orc = Actor(
    char="O",
    color=(63,127,63), 
    name="Orc", 
    ai_cls=HostileEnemy, 
    component=Fighter(hp=10, defense=0, power=3)
)
troll = Actor(
    char="T",
    color=(0,127,0), 
    name="Troll", 
    ai_cls=HostileEnemy, 
    component=Fighter(hp=16, defense=1, power=4)
)
boss = Actor(
    char="B",
    color=(255,255,255), 
    name="Boss", 
    ai_cls=HostileEnemy, 
    component=Fighter(hp=30, defense=2, power=5)
)
