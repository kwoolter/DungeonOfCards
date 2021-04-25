import random
from enum import Enum, auto


class Element(Enum):
    PHYSICAL = auto()
    MAGICAL = auto()
    # FIRE = 1
    # ICE = 2
    # WATER = 3


class CardFeature(Enum):
    ATTACK = auto()
    DEFEND = auto()
    QUICK = auto()
    HEAL = auto()
    DEAL = auto()
    UNBLOCKABLE = auto()


class Outcome(Enum):
    HIT = 1
    BLOCK = 2
    PARTIAL_BLOCK = 3


class CardType(Enum):
    BATTLE = 1
    LOOT = 2
    MAP = 3


class BaseCard():
    def __init__(self, name: str, type: str):
        # Properties
        self.name = name
        self.type = type

    def print(self):
        print(f"Card '{self.name}' ({self.type.name})")


class BattleCard(BaseCard):
    MAX_ATTACKS = 3
    MAX_BLOCKS = 3
    MAX_NEW_DEALS = 3

    def __init__(self, name: str):
        super().__init__(name, CardType.BATTLE)

        # Properties
        self.is_attack_unblockable = False
        self.is_quick = False
        self.new_card_count = 1

        self.attacks = {}
        self.blocks = {}
        self.heals = {}

    def print(self):
        print(f"Card '{self.name}' ({self.type.name}) "
              f"quick={self.is_quick} "
              f"new_cards={self.new_card_count} "
              f"unblockable={self.is_attack_unblockable}")

        for k, v in self.attacks.items():
            print(f"\tAttack {k}={v}")

        for k, v in self.blocks.items():
            print(f"\tBlock {k}={v}")

        for k, v in self.heals.items():
            print(f"\tHeal {k}={v}")

    def generate(self, level: int = 1):

        features_added = 0

        while features_added < level:

            feature = random.choice(list(CardFeature))

            if feature is CardFeature.ATTACK and len(self.attacks) < BattleCard.MAX_ATTACKS:
                e = random.choice(list(Element))
                self.attacks[e] = self.attacks.get(e, 0) + 1
            elif feature is CardFeature.DEFEND and len(self.blocks) < BattleCard.MAX_BLOCKS:
                e = random.choice(list(Element))
                self.blocks[e] = self.blocks.get(e, 0) + 1
            elif feature is CardFeature.UNBLOCKABLE and self.is_attack_unblockable is False and len(self.attacks) > 0:
                self.is_attack_unblockable = True
            elif feature is CardFeature.HEAL:
                outcome = random.choice(list(Outcome))
                self.heals[outcome] = self.heals.get(outcome, 0) + 1
            elif feature is CardFeature.QUICK and self.is_quick is False:
                self.is_quick = True
            elif feature is CardFeature.DEAL and self.new_card_count < BattleCard.MAX_NEW_DEALS:
                self.new_card_count += 1
            else:
                features_added -= 1

            features_added += 1


class LootCard(BaseCard):
    def __init__(self, name: str):
        super().__init__(name, CardType.LOOT)


def test():
    print(f"\nTesting {__file__}\n")

    for i in range(1, 10):
        c = BattleCard("Oi")
        c.generate(i)
        c.print()

    l = LootCard("Gold")
    l.print()


if __name__ == "__main__":
    test()
