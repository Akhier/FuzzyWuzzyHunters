import libtcodpy as libtcod
from random import randint

from components.ai import BasicMonster
from components.fighter import Fighter

from entity import Entity
from render_functions import RenderOrder


def create_orc(x, y):
    fighter_component = Fighter(
        hp=randint(18, 22), defense=0, power=4, xp=35)
    ai_component = BasicMonster()

    return Entity(x, y, 'o', libtcod.desaturated_green,
                  'Orc', blocks=True,
                  render_order=RenderOrder.ACTOR,
                  fighter=fighter_component,
                  ai=ai_component)


def create_troll(x, y):
    fighter_component = Fighter(
        hp=30, defense=2, power=randint(7, 9), xp=100)
    ai_component = BasicMonster()

    return Entity(x, y, 'T', libtcod.darker_green,
                  'Troll', blocks=True,
                  render_order=RenderOrder.ACTOR,
                  fighter=fighter_component,
                  ai=ai_component)
