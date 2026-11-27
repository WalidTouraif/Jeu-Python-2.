from entities import Character
from items import Consumable, Equipable


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.team = []
        self.inventory = []