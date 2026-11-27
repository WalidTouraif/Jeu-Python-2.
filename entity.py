from abc import ABC, abstractmethod
from typing import List


class Entity(ABC):
    def __init__(self, name: str, hp: int, attack: int, defense: int):
        self.name: str = name
        self.hp: int = hp
        self.maxHp: int = hp
        self.attack: int = attack
        self.defense: int = defense

    def IsAlive(self) -> bool:
        return self.hp > 0

    def TakeDamage(self, amount: int):
        # au minimum 1 degat
        degats = max(amount - self.defense, 1)
        self.hp = max(self.hp - degats, 0)

    def Heal(self, amount: int):
        self.hp = min(self.hp + amount, self.maxHp)

    def Attack(self, target: "Entity"):
        avant = target.hp
        target.TakeDamage(self.attack)
        print(self.name, "frappe", target.name, ":", avant - target.hp, "degats")

    @abstractmethod
    def PlayTurn(self, cibles: List["Entity"]):
        pass