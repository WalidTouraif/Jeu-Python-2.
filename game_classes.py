import random
from abc import ABC, abstractmethod
from typing import Dict, List


class Item(ABC):
    def __init__(self, name: str, description: str, drop_rate: float,
                 rarity: str, item_type: str, stats: Dict[str, int]):
        self.name: str = name
        self.description: str = description
        self.drop_rate: float = drop_rate      
        self.rarity: str = rarity
        self.item_type: str = item_type
        self.stats: Dict[str, int] = stats

    def __str__(self) -> str:
        return f"{self.name} ({self.rarity})"


class Equipable(Item):
    pass


class Consumable(Item):
    def Use(self, target: "Entity"):
        if "hp" in self.stats:
            target.Heal(self.stats["hp"])
        if "attack" in self.stats:
            target.attack += self.stats["attack"]
        if "defense" in self.stats:
            target.defense += self.stats["defense"]


class Entity(ABC):
    def __init__(self, name: str, hp: int, max_hp: int, attack: int, defense: int):
        self.name: str = name
        self.hp: int = hp
        self.max_hp: int = max_hp
        self.attack: int = attack
        self.defense: int = defense

    def __str__(self) -> str:
        if self.IsAlive():
            etat = f"PV {self.hp}/{self.max_hp}"
        else:
            etat = "KO"
        return f"{self.name} - {etat} - ATK {self.attack} - DEF {self.defense}"

    def IsAlive(self) -> bool:
        return self.hp > 0

    def TakeDamage(self, amount: int):
        degats = max(amount - self.defense, 1)    
        self.hp = max(self.hp - degats, 0)

    def Heal(self, amount: int):
        self.hp = min(self.hp + amount, self.max_hp)

    def Attack(self, target: "Entity") -> str:
        avant = target.hp
        target.TakeDamage(self.attack)
        message = f"{self.name} inflige {avant - target.hp} dégâts à {target.name}"
        if not target.IsAlive():
            message += f"\n{target.name} est KO"
        return message

    @abstractmethod
    def PlayTurn(self, cibles: List["Entity"]) -> str:
        pass


class Enemy(Entity):
    def __init__(self, name: str, hp: int, max_hp: int, attack: int, defense: int,
                 dropables: List[Item] = None):
        super().__init__(name, hp, max_hp, attack, defense)
        if dropables is None:
            dropables = []
        self.dropables: List[Item] = dropables

    def DropLoot(self) -> List[Item]:
        loot = []
        for item in self.dropables:
            if random.random() < item.drop_rate:
                loot.append(item)
        return loot

    def PlayTurn(self, cibles: List[Entity]) -> str:
        vivants = []
        for c in cibles:
            if c.IsAlive():
                vivants.append(c)
        if len(vivants) == 0:
            return ""
        return self.Attack(random.choice(vivants))


class Character(Entity):
    def __init__(self, name: str, hp: int, max_hp: int, attack: int, defense: int,
                 equipement: List[Equipable] = None):
        self.equipement: List[Equipable] = []
        super().__init__(name, hp, max_hp, attack, defense)
        if equipement is not None:
            self.equipement = list(equipement)

    def _bonus(self, stat: str) -> int:
        total = 0
        for item in self.equipement:
            total += item.stats.get(stat, 0)
        return total

    @property
    def attack(self) -> int:
        return self._attack + self._bonus("attack")

    @attack.setter
    def attack(self, value: int):
        self._attack = value - self._bonus("attack")

    @property
    def defense(self) -> int:
        return self._defense + self._bonus("defense")

    @defense.setter
    def defense(self, value: int):
        self._defense = value - self._bonus("defense")

    def IsSlotAvailable(self, slot_name: str) -> bool:
        return self.GetEquipment(slot_name) is None

    def GetEquipment(self, slot_name: str):
        for item in self.equipement:
            if item.item_type == slot_name:
                return item
        return None

    def EquipItem(self, item: Equipable):
        if self.IsSlotAvailable(item.item_type):
            self.equipement.append(item)

    def UnequipItem(self, item: Equipable):
        if item in self.equipement:
            self.equipement.remove(item)

    def ProjectDamage(self, target: Entity) -> int:
        return max(self.attack - target.defense, 1)

    def PlayTurn(self, cibles: List[Entity]) -> str:
        for c in cibles:
            if c.IsAlive():
                return self.Attack(c)
        return ""