import libtcodpy as libtcod
from random import randint

from components.item import Item
from components.stairs import Stairs

from entity import Entity
from game_messages import Message
from item_functions import cast_confuse, cast_fireball, cast_lightning, heal
from map_objects.tile import Tile
from map_objects.monsters import (
    create_naked_mole_rat, create_naked_mole_rat_queen, create_sphynx,
    create_hippo, create_elephant, create_fuzzy_wuzzy)
from random_utils import from_dungeon_level, random_choice_from_dict
from render_functions import RenderOrder


class GameMap:

    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)]
                 for x in range(self.width)]

        return tiles

    def make_map(self, player, entities):
        for y in range(2, self.height - 2):
            for x in range(2, self.width - 2):
                chance = randint(1, 100)
                if chance <= 65:
                    self.tiles[x][y].blocked = False
        self.process_map()
        self.process_map()
        self.place_entities(entities)
        starttile = False
        for y in range(2, self.height - 2):
            for x in range(2, self.width - 2):
                if not starttile and not self.is_blocked(x, y):
                    starttile = (x, y)
        player.x = starttile[0]
        player.y = starttile[1]
        endtile = False
        for y in range(self.height - 2, 2, -1):
            for x in range(self.width - 2, 2, -1):
                if not endtile and not self.is_blocked(x, y):
                    endtile = (x, y)
        if self.dungeon_level < 5:
            stairs_component = Stairs(self.dungeon_level + 1)
            down_stairs = Entity(
                endtile[0], endtile[1], '>',
                libtcod.white, 'Stairs', render_order=RenderOrder.STAIRS,
                stairs=stairs_component)
            entities.append(down_stairs)
        else:
            entities.append(create_fuzzy_wuzzy(endtile[0], endtile[1]))

        if not self.check_stairs_reachable(player, endtile):
            self.make_map(player, entities)

    def process_map(self):
        newtiles = self.initialize_tiles()
        for y in range(2, self.height - 2):
            for x in range(2, self.width - 2):
                newtiles[x][y].blocked = False
                walls = self.get_walls(x, y)
                if walls >= 5:
                    newtiles[x][y].blocked = True
                elif walls == 0:
                    newtiles[x][y].blocked = True
                newtiles[x][y].block_sight = newtiles[x][y].blocked
        self.tiles = newtiles

    def check_stairs_reachable(self, player, endtile):
        star = libtcod.map_new(self.width, self.height)

        for y1 in range(self.height):
            for x1 in range(self.width):
                libtcod.map_set_properties(
                    star, x1, y1, not self.tiles[x1][y1].block_sight,
                    not self.tiles[x1][y1].blocked)

        path = libtcod.path_new_using_map(star, 1)
        libtcod.path_compute(path, player.x, player.y, endtile[0], endtile[1])

        if libtcod.path_is_empty(path):
            return False
        return True

    def get_walls(self, x, y):
        wallcount = 0
        if self.is_blocked(x - 1, y - 1):
            wallcount += 1
        if self.is_blocked(x, y - 1):
            wallcount += 1
        if self.is_blocked(x + 1, y - 1):
            wallcount += 1
        if self.is_blocked(x - 1, y + 1):
            wallcount += 1
        if self.is_blocked(x, y + 1):
            wallcount += 1
        if self.is_blocked(x + 1, y + 1):
            wallcount += 1
        if self.is_blocked(x - 1, y):
            wallcount += 1
        if self.is_blocked(x, y):
            wallcount += 1
        if self.is_blocked(x + 1, y):
            wallcount += 1
        return wallcount

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def place_entities(self, entities):
        max_monsters_per_room = from_dungeon_level(
            [[100, 1], [75, 2], [50, 3], [25, 4]], self.dungeon_level)
        max_items_per_room = from_dungeon_level(
            [[20, 1], [10, 4]], self.dungeon_level)

        number_of_monsters = randint(int(max_monsters_per_room / 2),
                                     max_monsters_per_room)
        number_of_items = randint(int(max_items_per_room), max_items_per_room)

        monster_chances = {
            'nmrat': from_dungeon_level(
                [[100, 1], [10, 2], [0, 3]], self.dungeon_level),
            'nmratqueen': from_dungeon_level(
                [[1, 1], [0, 2]], self.dungeon_level),
            'sphynx': from_dungeon_level(
                [[10, 1], [100, 2]], self.dungeon_level),
            'hippo': from_dungeon_level(
                [[1, 2], [100, 3], [5, 4], [0, 5]], self.dungeon_level),
            'elephant': from_dungeon_level(
                [[1, 3], [100, 4]], self.dungeon_level)
        }
        item_chances = {
            'healing_potion': 35,
            'lightning_scroll': from_dungeon_level(
                [[15, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level(
                [[20, 2]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level(
                [[25, 3]], self.dungeon_level)
        }

        i = 0
        while i < number_of_monsters:
            # Choose a random location in the room
            x = randint(1, self.width - 2)
            y = randint(1, self.height - 2)

            if not any([entity for entity in entities
                        if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'nmrat':
                    monster = create_naked_mole_rat(x, y)
                elif monster_choice == 'nmratqueen':
                    monster = create_naked_mole_rat_queen(x, y)
                elif monster_choice == 'sphynx':
                    monster = create_sphynx(x, y)
                elif monster_choice == 'hippo':
                    monster = create_hippo(x, y)
                else:
                    monster = create_elephant(x, y)

                i += 1
                entities.append(monster)

        i = 0
        while i < number_of_items:
            x = randint(1, self.width - 2)
            y = randint(1, self.height - 2)

            if not any([entity for entity in entities
                        if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion',
                                  render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(
                        use_function=cast_fireball, targeting=True,
                        targeting_message=Message(
                            'Left-click a target tile for the fireball, or ' +
                            'right-click to cancel.', libtcod.light_cyan),
                        damage=25, radius=3)
                    item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll',
                                  render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(
                        use_function=cast_confuse, targeting=True,
                        targeting_message=Message(
                            'Left-click an enemy to confuse it, or ' +
                            'right-click to cancel.', libtcod.light_cyan))
                    item = Entity(
                        x, y, '#', libtcod.light_pink, 'Confusion Scroll',
                        render_order=RenderOrder.ITEM, item=item_component)
                else:
                    item_component = Item(use_function=cast_lightning,
                                          damage=40, maximum_range=5)
                    item = Entity(
                        x, y, '#', libtcod.yellow, 'Lightning Scroll',
                        render_order=RenderOrder.ITEM, item=item_component)

                i += 1
                entities.append(item)

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message(
            'You take a moment to rest, and recover your strength.',
            libtcod.light_violet))

        return entities
