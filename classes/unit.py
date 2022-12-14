from __future__ import annotations
from abc import ABC, abstractmethod
from classes.equipment import Weapon, Armor
from classes.classes import UnitClass
from random import randint


class BaseUnit(ABC):
    """
    Базовый класс юнита.
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass.
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon: Weapon
        self.armor: Armor
        self._is_skill_used = False

    @property
    def health_points(self) -> float:
        # Возвращаем аттрибут hp в красивом виде.
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        # Возвращаем аттрибут stamina в красивом виде.
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon) -> str:
        # Присваиваем нашему герою новое оружие.
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        # Одеваем новую броню.
        self.armor = armor
        return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        # Эта функция должна содержать:
        # логику расчёта урона игрока,
        # логику расчёта брони цели, если у защищающегося не хватает выносливости, его броня игнорируется,
        # здесь же происходит уменьшение выносливости атакующего при ударе,
        # и уменьшение выносливости защищающегося при использовании брони.
        damage = round(self.weapon.damage * self.unit_class.attack, 1)
        self.stamina = round(self.stamina - self.weapon.stamina_per_hit * self.unit_class.stamina, 1)

        if target.stamina > target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina = round(target.stamina_points - target.armor.stamina_per_turn * target.unit_class.stamina, 1)
            damage = round(damage - target.armor.defence * target.unit_class.armor, 1)

        # После всех расчетов цель получает урон - target.get_damage(damage)
        damage = damage if damage > 0 else 0
        if damage > 0:
            target.get_damage(damage)

        # и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде.
        return damage

    def get_damage(self, damage: float):
        # Получение урона целью.
        # Присваиваем новое значение для аттрибута self.hp.
        if damage > 0:
            hp = round(self.hp - damage, 1)
            self.hp = hp if hp > 0 else 0

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        Этот метод будет переопределен ниже.
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        Метод использования умения.
        Если умение уже использовано, возвращаем строку "Навык использован",
        если умение не использовано, тогда выполняем функцию self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернет нам строку, которая характеризует выполнение умения.
        """
        if self._is_skill_used:
            return "Навык уже использован."
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара,
        вызывается функция self._count_damage(target), а также возвращается результат в виде строки.
        """
        if self.stamina >= self.weapon.stamina_per_hit * self.unit_class.stamina:
            damage = self._count_damage(target)
            if damage:
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит " \
                       f"{damage} урона."
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его " \
                   f"останавливает."
        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар соперника
        Должна содержать логику применения соперником умения (он должен делать это автоматически и только 1 раз за бой)
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется функция _count_damage(target)
        """
        if randint(0, 10) == 10 and not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina:
            return self.use_skill(target)

        if self.stamina >= self.weapon.stamina_per_hit * self.unit_class.stamina:
            damage = self._count_damage(target)
            if damage:
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам " \
                       f"{damage} урона."
            return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его " \
                   f"останавливает."
        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
