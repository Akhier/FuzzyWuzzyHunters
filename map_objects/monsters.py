import libtcodpy as libtcod
from random import randint

from components.ai import BasicMonster
from components.fighter import Fighter

from entity import Entity
from render_functions import RenderOrder


def calculate_xp(hp, defense, power):
    if defense < 1:
        defense = 1
    return hp * defense + power * power


def create_orc(x, y):
    fighter_component = Fighter(
        hp=20, defense=0, power=4, xp=35)
    ai_component = BasicMonster()

    return Entity(x, y, 'o', libtcod.desaturated_green,
                  'Orc', blocks=True,
                  render_order=RenderOrder.ACTOR,
                  fighter=fighter_component,
                  ai=ai_component)


def create_troll(x, y):
    fighter_component = Fighter(
        hp=30, defense=2, power=8, xp=100)
    ai_component = BasicMonster()

    return Entity(x, y, 'T', libtcod.darker_green,
                  'Troll', blocks=True,
                  render_order=RenderOrder.ACTOR,
                  fighter=fighter_component,
                  ai=ai_component)


def create_naked_mole_rat(x, y):
    hp = randint(3, 6)
    defense = 0
    power = 1
    xp = calculate_xp(hp, defense, power)
    fighter_component = Fighter(hp, defense, power, xp)
    ai_component = BasicMonster()

    return Entity(x, y, 'n', libtcod.sepia_light,
                  'Naked Mole Rat', blocks=True,
                  render_order=RenderOrder.ACTOR,
                  fighter=fighter_component,
                  ai=ai_component)


def create_naked_mole_rat_queen(x, y):
    hp = randint(30, 60)
    defense = 2
    power = 3
    xp = calculate_xp(hp, defense, power)
    fighter_component = Fighter(hp, defense, power, xp)
    ai_component = BasicMonster()

    return Entity(x, y, 'n', libtcod.sepia,
                  'Naked Mole Rat Queen', blocks=True,
                  render_order=RenderOrder.ACTOR,
                  fighter=fighter_component,
                  ai=ai_component)


def create_sphynx(x, y):
    hp = 20
    defense = 0
    power = randint(3, 5)
    xp = calculate_xp(hp, defense, power)
    fighter_component = Fighter(hp, defense, power, xp)
    ai_component = BasicMonster()

    return Entity(x, y, 'c', libtcod.sepia_lighter,
                  'Sphynx', blocks=True,
                  render_order=RenderOrder.ACTOR,
                  fighter=fighter_component,
                  ai=ai_component)


def create_hippo(x, y):
    hp = 30
    defense = 2
    power = 8
    xp = calculate_xp(hp, defense, power)
    fighter_component = Fighter(hp, defense, power, xp)
    ai_component = BasicMonster()

    return Entity(x, y, 'H', libtcod.grey,
                  'Hippo', blocks=True,
                  render_order=RenderOrder.ACTOR,
                  fighter=fighter_component,
                  ai=ai_component)


def create_elephant(x, y):
    hp = randint(38, 45)
    defense = randint(2, 3)
    power = 8
    xp = calculate_xp(hp, defense, power)
    fighter_component = Fighter(hp, defense, power, xp)
    ai_component = BasicMonster()

    return Entity(x, y, 'E', libtcod.grey_dark,
                  'Elephant', blocks=True,
                  render_order=RenderOrder.ACTOR,
                  fighter=fighter_component,
                  ai=ai_component)


def create_fuzzy_wuzzy(x, y):
    hp = 60
    defense = 4
    power = 10
    xp = calculate_xp(hp, defense, power)
    fighter_component = Fighter(hp, defense, power, xp)
    ai_component = BasicMonster()

    return Entity(x, y, 'B', libtcod.silver,
                  'Fuzzy Wuzzy', blocks=True,
                  render_order=RenderOrder.ACTOR,
                  fighter=fighter_component,
                  ai=ai_component)
