from abc import ABC
from typing import Dict


class Item(ABC):
    def __init__(self, name: str, description: str, dropRate: int,
                 rarity: str, item_type: str, stats: Dict[str, int]):
        self.name: str = name
        self.description: str = description
        self.dropRate: int = dropRate
        self.rarity: str = rarity
        self.item_type: str = item_type
        self.stats: Dict[str, int] = stats


class Equipable(Item):
    pass


class Consumable(Item):
    def Use(self, target):
        # la potion soigne ou booste la cible
        if "hp" in self.stats:
            target.Heal(self.stats["hp"])
        if "attack" in self.stats:
            target.attack += self.stats["attack"]
        if "defense" in self.stats:
            target.defense += self.stats["defense"]