class Item:
    def __init__(self, name, description, rarity, item_type, stats, drop_rate=0):
        self.name = name
        self.description = description
        self.rarity = rarity
        self.item_type = item_type      
        self.stats = stats             
        self.drop_rate = drop_rate     


class Equipable(Item):
    pass                              


class Consumable(Item):
    def use(self, target):
        if "hp" in self.stats:
            target.heal(self.stats["hp"])
        if "attack" in self.stats:
            target.attack += self.stats["attack"]
        if "defense" in self.stats:
            target.defense += self.stats["defense"]



DROP_RATES = {"commune": 70, "rare": 25, "épique": 4, "légendaire": 1}


def creer_item(data):

    description = data["item_type"] + " " + data["rarity"]
    rate = DROP_RATES.get(data["rarity"], 0)
    if data["consumable"]:
        return Consumable(data["name"], description, data["rarity"],
                          data["item_type"], data["effect"], rate)
    return Equipable(data["name"], description, data["rarity"],
                     data["item_type"], data["effect"], rate)