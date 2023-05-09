from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:

    def __init__(self, armor):
        self.name = armor['name']
        self.defence = armor['defence']
        self.stamina = armor['stamina_per_turn']


@dataclass
class Weapon:

    def __init__(self, weapon):
        self.name = weapon['name']
        self.min_damage = weapon['min_damage']
        self.max_damage = weapon['max_damage']
        self.stamina = weapon['stamina_per_hit']

    @property
    def damage(self):
        pass


@dataclass
class EquipmentData:
    weapons: list
    armor: list


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        for i in self.equipment.weapons:
            if i['name'] == weapon_name:
                return Weapon(i)

    def get_armor(self, armor_name) -> Armor:
        for i in self.equipment.armor:
            if i['name'] == armor_name:
                return Armor(i)

    @property
    def get_weapons_names(self) -> list:
        return [i["name"] for i in self.equipment.weapons]

    @property
    def get_armors_names(self) -> list:
        return [i["name"] for i in self.equipment.armor]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        with open("data/character_values/equipment.json", encoding='utf-8') as equipment_file:
            data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load({"weapons": data["weapon"], "armor": data["armor"]})
        except marshmallow.exceptions.ValidationError:
            raise ValueError
