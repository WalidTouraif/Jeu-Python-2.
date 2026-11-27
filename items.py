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
        if "hp" in self.stats:
            target.Heal(self.stats["hp"])
        if "attack" in self.stats:
            target.attack += self.stats["attack"]
        if "defense" in self.stats:
            target.defense += self.stats["defense"]


# Les objets du jeu
ITEMS = [
    Consumable("Potion de soin", "Rend 50 PV", 50, "commune", "consommable", {"hp": 50}),
    Consumable("Elixir de force", "+10 attaque", 20, "rare", "consommable", {"attack": 10}),
    Equipable("Epee en fer", "Une epee", 30, "commune", "arme", {"attack": 5}),
    Equipable("Bouclier en bois", "Un bouclier", 30, "commune", "armure", {"defense": 3}),
    Equipable("Anneau magique", "Un anneau", 10, "rare", "accessoire", {"attack": 10, "defense": 5}),
]