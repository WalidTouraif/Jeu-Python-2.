import random


class Entity:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        degats = max(amount - self.get_defense(), 1)
        self.hp = max(self.hp - degats, 0)
        return degats

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)

    def attack_target(self, target):
        degats = target.take_damage(self.get_attack())
        print(f"{self.name} inflige {degats} degats a {target.name} (PV : {target.hp})")

    def play_turn(self, cibles):
        # méthode abstraite : chaque enfant doit la réécrire
        raise NotImplementedError("play_turn doit être écrit dans la classe enfant")


class Enemy(Entity):
    def __init__(self, name, hp, attack, defense, dropables):
        super().__init__(name, hp, attack, defense)
        self.dropables = dropables      # liste d'Item

    def drop_loot(self):
        loot = []
        for item in self.dropables:
            if random.randint(1, 100) <= item.drop_rate:
                loot.append(item)
        return loot

    def play_turn(self, cibles):
        vivants = [c for c in cibles if c.is_alive()]
        if len(vivants) > 0:
            self.attack_target(random.choice(vivants))


class Character(Entity):
    def __init__(self, name, hp, attack, defense):
        super().__init__(name, hp, attack, defense)
        self.equipement = []            # liste d'Equipable

    # attack et defense "calculés" (les /attack et /defense du diagramme)
    def get_attack(self):
        bonus = 0
        for item in self.equipement:
            bonus += item.stats.get("attack", 0)
        return self.attack + bonus

    def get_defense(self):
        bonus = 0
        for item in self.equipement:
            bonus += item.stats.get("defense", 0)
        return self.defense + bonus

    def is_slot_available(self, slot_name):
        for item in self.equipement:
            if item.item_type == slot_name:
                return False
        return True

    def get_equipment(self, slot_name):
        for item in self.equipement:
            if item.item_type == slot_name:
                return item
        return None

    def equip_item(self, item):
        if self.is_slot_available(item.item_type):
            self.equipement.append(item)
            print(f"{self.name} équipe {item.name}")
            return True
        print(f"{self.name} a déjà un objet de type {item.item_type}")
        return False

    def unequip_item(self, item):
        if item in self.equipement:
            self.equipement.remove(item)

    def project_damage(self, target):
        # combien de dégâts on ferait à la cible, sans l'attaquer
        return max(self.get_attack() - target.get_defense(), 1)

    def play_turn(self, cibles):
        vivants = [c for c in cibles if c.is_alive()]
        if len(vivants) > 0:
            self.attack_target(vivants[0])