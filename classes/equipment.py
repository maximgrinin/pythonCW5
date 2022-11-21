from dataclasses import dataclass
from typing import List, Optional
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    # Содержит 2 списка - с оружием и с бронёй.
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:
    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Optional[Weapon]:
        # Возвращает объект оружия по имени.
        return next(filter(lambda weapon: weapon.name == weapon_name, self.equipment.weapons), None)

    def get_armor(self, armor_name) -> Optional[Armor]:
        # Возвращает объект брони по имени.
        return next(filter(lambda armor: armor.name == armor_name, self.equipment.armors), None)

    def get_weapons_names(self) -> list:
        # Возвращаем список с оружием.
        # return {weapon.name: weapon for weapon in self.equipment.weapons}
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list:
        # Возвращаем список с бронёй.
        # return {armor.name: armor for armor in self.equipment.armors}
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # Этот метод загружает json в переменную EquipmentData.
        with open("data/equipment.json", encoding="utf-8") as equipment_file:
            data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
