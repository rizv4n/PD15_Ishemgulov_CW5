import json
from dataclasses import dataclass

from data.character.equipment import Equipment
from data.character.unit import PlayerUnit, EnemyUnit
from data.character.skills import Skill, unit_skills

equip = Equipment()


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


class Heroes:
    def __init__(self, player: PlayerUnit, enemy: EnemyUnit):
        self.player = player
        self.enemy = enemy


def get_classes() -> dict:
    with open('data/character_values/classes.json', encoding='utf-8') as file:

        classes = json.load(file)

        WarriorClass = UnitClass(**classes['warrior'])
        WarriorClass.skill = unit_skills.get(WarriorClass.skill)

        ThiefClass = UnitClass(**classes['thief'])
        ThiefClass.skill = unit_skills.get(ThiefClass.skill)

        return {WarriorClass.name: WarriorClass, ThiefClass.name: ThiefClass}


def get_heroes(player_characters, enemy_characters):

    player = PlayerUnit(player_characters[0], get_classes()[player_characters[1]])
    player.equip_weapon(equip.get_weapon(player_characters[2]))
    player.equip_armor(equip.get_armor(player_characters[3]))

    enemy = EnemyUnit(enemy_characters[0], get_classes()[enemy_characters[1]])
    enemy.equip_weapon(equip.get_weapon(enemy_characters[2]))
    enemy.equip_armor(equip.get_armor(enemy_characters[3]))

    return player, enemy

