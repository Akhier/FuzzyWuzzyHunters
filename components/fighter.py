import libtcodpy as libtcod
from random import randint

from game_messages import Message


class Fighter:
    def __init__(self, hp, defense, power, xp=0, dodge_chance=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp
        self.dodge_chance = dodge_chance

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []
        accuracy = randint(1, 100)
        if accuracy > target.fighter.dodge_chance:
            chance = randint(1, 100)
            if chance <= 25:
                power = self.power - 1
                if power < 1:
                    power = 1
            elif chance <= 95:
                power = self.power
            else:
                power = self.power + 1
            damage = power - target.fighter.defense

            if damage > 0:
                results.append(
                    {'message': Message(
                        '{0} attacks {1} for {2} hit points.'.format(
                            self.owner.name.capitalize(), target.name,
                            str(damage)), libtcod.white)})
                results.extend(target.fighter.take_damage(damage))
            else:
                results.append(
                    {'message': Message(
                        '{0} attacks {1} but does no damage'.format(
                            self.owner.name.capitalize(),
                            target.name), libtcod.white)})
        else:
            results.append(
                {'message': Message(
                    '{0} misses {1} with their attack.'.format(
                        self.owner.name.capitalize(),
                        target.name), libtcod.light_blue)})

        return results
