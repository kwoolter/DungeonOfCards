import random
from enum import Enum, auto

# Types of attack and block elements
class Element(Enum):
    PHYSICAL = auto()
    MAGICAL = auto()
    # FIRE = 1
    # ICE = 2
    # WATER = 3

# Enum for teh different types of features that can be added to a BattleCard
class CardFeature(Enum):
    ATTACK = auto()
    DEFEND = auto()
    QUICK = auto()
    HEAL = auto()
    DEAL = auto()
    UNBLOCKABLE = auto()


class Outcome(Enum):
    HIT = auto()
#    BLOCK = auto()
#    PARTIAL_BLOCK = auto()


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
        self.new_card_count = 0

        self.attacks = {}
        self.blocks = {}
        self.heals = {}

    def print(self):
        print(f"Card '{self.name}' ({self.type.name}) "
              f"quick={self.is_quick} "
              f"new_cards={self.new_card_count} "
              f"unblockable={self.is_attack_unblockable}")

        for k, v in self.attacks.items():
            print(f"\tAttack {k.name}={v}")

        for k, v in self.blocks.items():
            print(f"\tBlock {k.name}={v}")

        for k, v in self.heals.items():
            print(f"\tHeal {k}={v}")

    def generate(self, level: int = 1):

        # How many features have been added to this card so far i.e. 0
        features_added = 0

        # Random weightings for features...
        #         ATTACK
        #         DEFEND
        #         QUICK
        #         HEAL
        #         DEAL
        #         UNBLOCKABLE
        weights = [10, 10, 4, 3, 1, 3]

        # Keep adding features to the Battle Card until we reach the required level...
        while features_added < level:

            # Pick a weighted random feature that we want to add
            feature = random.choices(list(CardFeature), weights=weights, k=1)[0]

            # If it is an attack and we haven't hit the max number of attacks..
            if feature is CardFeature.ATTACK and len(self.attacks) < BattleCard.MAX_ATTACKS:
                e = random.choice(list(Element))
                self.attacks[e] = self.attacks.get(e, 0) + 1

            # If it is a block and we haven't hit the max number of block..
            elif feature is CardFeature.DEFEND and len(self.blocks) < BattleCard.MAX_BLOCKS:
                e = random.choice(list(Element))
                self.blocks[e] = self.blocks.get(e, 0) + 1

            # If it is an unblockable attack, and we are not already unblockable, and we have at least 1 attack...
            elif feature is CardFeature.UNBLOCKABLE and self.is_attack_unblockable is False and len(self.attacks) > 0:
                self.is_attack_unblockable = True

            # If it is a heal feature...
            elif feature is CardFeature.HEAL:
                outcome = random.choice(list(Outcome))
                self.heals[outcome] = self.heals.get(outcome, 0) + 1

            # If it is a quick feature and we are not already quick...
            elif feature is CardFeature.QUICK and self.is_quick is False:
                self.is_quick = True

            # If it is a card dealing feature and we haven't hit the cap for this feature...
            elif feature is CardFeature.DEAL and self.new_card_count < BattleCard.MAX_NEW_DEALS:
                self.new_card_count += 1

            # Else we failed to add a new feature so off set the increment that is about to happen!!!!
            else:
                features_added -= 1

            # We think we added a new feature!
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
