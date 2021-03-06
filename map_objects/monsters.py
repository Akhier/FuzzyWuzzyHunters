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


def create_naked_mole_rat(x, y):
    hp = randint(3, 6)
    defense = 0
    power = 1
    xp = calculate_xp(hp, defense, power)
    fighter_component = Fighter(hp, defense, power, xp)
    ai_component = BasicMonster()

    return Entity(x, y, 'n', libtcod.light_sepia,
                  'Naked Mole Rat', blocks=True,
                  render_order=RenderOrder.ACTOR,
                  fighter=fighter_component,
                  ai=ai_component)


def create_naked_mole_rat_queen(x, y):
    chance = -1
    while chance < 0:
        chance = 0
        for i in range(6):
            chance += randint(1, 10)
        chance -= 30
    hp = 30 + chance
    defense = 2
    power = int(hp / 10)
    xp = calculate_xp(hp, defense, power)
    fighter_component = Fighter(hp, defense, power, xp)
    ai_component = BasicMonster()
    if hp == 30:
        name = 'Perfect Dire Naked Mole Rate Queen'
    elif hp >= 20:
        name = 'Dire Naked Mole Rat Queen'
    else:
        name = 'Naked Mole Rat Queen'

    return Entity(x, y, 'n', libtcod.sepia, name, blocks=True,
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

    return Entity(x, y, 'c', libtcod.lighter_sepia,
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

    return Entity(x, y, 'E', libtcod.dark_grey,
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
