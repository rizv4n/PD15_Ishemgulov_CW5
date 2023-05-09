from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):

    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        return self.user.name

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self):
        return self.user.unit_class.max_stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:

        self.user = user
        self.target = target

        if self._is_stamina_enough:
            return self.skill_effect()

        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name = "Свирепый пинок"
    stamina = 6
    damage = 12

    def skill_effect(self):

        self.user.unit_class.max_stamina -= self.stamina
        self.target.unit_class.max_health -= self.damage

        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона."


class HardShot(Skill):
    name = "Мощный укол"
    stamina = 5
    damage = 15

    def skill_effect(self):

        self.user.unit_class.max_stamina -= self.stamina
        self.target.unit_class.max_health -= self.damage

        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона."


unit_skills = {
    FuryPunch().name: FuryPunch(),
    HardShot().name: HardShot()
}
