from __future__ import annotations

import random
from abc import ABC, abstractmethod
from data.character.equipment import Weapon, Armor
from random import uniform
from typing import Optional


class BaseUnit(ABC):

    def __init__(self, name: str, unit_class):
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = Weapon
        self.armor = Armor
        self._is_skill_used = False

    @property
    def health_points(self):
        return self.hp

    @property
    def stamina_points(self):
        return self.stamina

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:

        weapon_damage = uniform(self.weapon.min_damage, self.weapon.max_damage)
        unit_damage = weapon_damage*self.unit_class.attack

        if target.unit_class.max_stamina > target.armor.stamina:

            target_armor = target.armor.defence*target.unit_class.armor
            target.unit_class.max_stamina -= target.armor.stamina

        else:

            target_armor = target.armor.defence

        damage = round(unit_damage - target_armor, 1)
        target.get_damage(damage)
        self.unit_class.max_stamina -= self.weapon.stamina

        return damage

    def get_damage(self, damage: int) -> Optional[int]:
        self.unit_class.max_health = round((self.unit_class.max_health - damage), 1)
        return self.unit_class.max_health

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        pass

    def use_skill(self, target: BaseUnit) -> str:

        if not self._is_skill_used:
            self._is_skill_used = True
            if self.unit_class.max_stamina > self.unit_class.skill.stamina:
                result = self.unit_class.skill.use(user=self, target=target)
                return result
            else:
                return f"{self.name} попытался использовать умение {self.unit_class.skill.name}, но у него не хватило выносливости."
        else:
            return "Навык использован"


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:

        if self.unit_class.max_stamina < self.weapon.stamina:

            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        if target.unit_class.max_stamina < target.armor.stamina:
            damage = self._count_damage(target)

            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."

        else:
            damage = self._count_damage(target)

            return f"{self.name} используя {self.weapon.name} наносит {damage} урона."


class EnemyUnit(BaseUnit):

    for_skill_randomize = 0  # счетчик раундов
    randomize_in = [5, 11]  # диапазон раундов, когда Enemy может применить Skill

    def hit(self, target: BaseUnit) -> str:

        if not self._is_skill_used:
            self.for_skill_randomize += 1

            if self.for_skill_randomize in self.randomize_in:
                check = random.choices([True, False])

                if check[0]:
                    self.use_skill(target)

            if self.for_skill_randomize == self.randomize_in[1]:
                self.use_skill(target)

        if self.unit_class.max_stamina < self.weapon.stamina:

            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        if target.unit_class.max_stamina < target.armor.stamina:
            damage = self._count_damage(target)

            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."

        else:
            damage = self._count_damage(target)

            return f"{self.name} используя {self.weapon.name} наносит {damage} урона."
