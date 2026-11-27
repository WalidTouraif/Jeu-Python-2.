import random


class Entity:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        degats = max(amount - self.defense, 1)
        self.hp = max(self.hp - degats, 0)
        return degats

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)

    def attack_target(self, target):
        degats = target.take_damage(self.attack)
        print(self.name, "frappe", target.name, "-", degats, "PV")

    def play_turn(self, cibles):
        pass