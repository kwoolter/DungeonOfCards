from enum import Enum


class Element(Enum):
    FIRE = 1
    ICE = 2
    WATER = 3


class Outcomes(Enum):
    HIT = 1
    BLOCK = 2
    PARTIAL_BLOCK = 3

class CardTypes(Enum):
    BATTLE = 1
    LOOT = 2
    MAP = 3


class BaseCard():
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
        self.is_attack_blockable = False
        self.is_speed_up = False

        self.attacks = {Element.FIRE: 0,
                        Element.WATER: 0}

        self.blocks = {Element.FIRE: 0,
                       Element.WATER: 0}

        self.heals = {}

    def print(self):
        print(f"Card '{self.name}' ({self.type.name})")


class BattleCard(BaseCard):
    def __init__(self, name : str):
        super().__init__(name, CardTypes.BATTLE)

class LootCard(BaseCard):
    def __init__(self, name : str):
        super().__init__(name, CardTypes.LOOT)

def test():
    print(f"\nTesting {__file__}\n")

    c = BattleCard("Oi")
    c.print()

    l = LootCard("Gold")
    l.print()

if __name__ == "__main__":
    test()
