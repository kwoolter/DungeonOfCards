import random

from .doc_enums import *


class BaseCard():
    def __init__(self, name: str, type: str):
        # Properties
        self.name = name
        self.type = type
        self.link_id = 0

    def print(self):
        print(f"Card '{self.name}' ({self.type.name})")


class BattleCard(BaseCard):
    MAX_ATTACKS = 3
    MAX_BLOCKS = 3
    MAX_NEW_DEALS = 3

    PLAYER_CARD_EFFECTS = [Effect.INVINCIBLE, Effect.BLESSED]
    ENEMY_CARD_EFFECTS = [Effect.BLIND, Effect.CONFUSED, Effect.DECAY, Effect.BURNING, Effect.SLEEP]

    def __init__(self, name: str):
        super().__init__(name, CardType.BATTLE)

        # Properties
        self.is_attack_unblockable = False
        self.is_quick = False
        self.new_card_count = 0

        self.attacks = {}
        self.blocks = {}
        self.heals = {}
        self.effects = {}

    def __str__(self):
        text = f"Battle Card '{self.name}': " \
               f"quick={self.is_quick} " \
               f"new_cards={self.new_card_count} " \
               f"unblockable={self.is_attack_unblockable}"
        return text

    def print(self):
        print(str(self))

        for k, v in self.attacks.items():
            print(f"\tAttack {k.name}={v}")

        for k, v in self.blocks.items():
            print(f"\tBlock {k.name}={v}")

        for k, v in self.heals.items():
            print(f"\tHeal {k}={v}")

        for k, v in self.effects.items():
            print(f"\tEffect {k}={v}")

    def generate(self, level: int = 1, is_player_card: bool = False):

        # Properties
        self.is_attack_unblockable = False
        self.is_quick = False
        self.new_card_count = 0

        self.attacks = {}
        self.blocks = {}
        self.heals = {}
        self.effects = {}

        # How many features have been added to this card so far i.e. 0
        features_added = 0

        # Random weightings for features...
        weights = [
            10,  # ATTACK MAGIC
            10,  # ATTACK MELEE
            10,  # DEFEND MAGIC
            10,  # DEFEND MELEE
            4,  # QUICK
            3,  # HEAL
            3,  # DEAL
            3,  # UNBLOCKABLE
            3  # EFFECT
        ]

        # Keep adding features to the Battle Card until we reach the required level...
        while features_added < level:

            # Pick a weighted random feature that we want to add
            feature = random.choices(list(CardFeature), weights=weights, k=1)[0]

            # If it is an attack and we haven't hit the max number of attacks..
            if feature in (CardFeature.ATTACK_MAGIC, CardFeature.ATTACK_MELEE) and len(self.attacks) < BattleCard.MAX_ATTACKS:
                self.attacks[feature] = self.attacks.get(feature, 0) + 1

            # If it is a block and we haven't hit the max number of block..
            elif feature in (CardFeature.BLOCK_MAGIC, CardFeature.BLOCK_MELEE) and len(self.blocks) < BattleCard.MAX_BLOCKS:
                self.blocks[feature] = self.blocks.get(feature, 0) + 1

            # If it is an unblockable attack feature
            # and we are not already unblockable
            # and we have at least 1 attack...
            elif feature is CardFeature.UNBLOCKABLE and \
                    self.is_attack_unblockable is False and \
                    len(self.attacks) > 0:

                self.is_attack_unblockable = True

            # If it is a heal feature...
            elif feature is CardFeature.HEAL:
                # Store heal value in a dummy placeholder for now
                outcome = "DUMMY"
                self.heals[outcome] = self.heals.get(outcome, 0) + 1

            # If it is a quick feature
            # and we are building a player card
            # and we are not already quick
            # and we have some attacks to make quick...
            elif feature is CardFeature.QUICK and \
                    is_player_card is True and \
                    self.is_quick is False and \
                    len(self.attacks) > 0:
                self.is_quick = True

            # If it is a card dealing feature and we haven't hit the cap for this feature...
            elif feature is CardFeature.DEAL and self.new_card_count < BattleCard.MAX_NEW_DEALS:
                self.new_card_count += 1

            # If adding an effect feature and if no effects yet added...
            elif feature is CardFeature.EFFECT and len(self.effects) == 0:
                # Store random effect against a dummy outcome placeholder for now
                outcome = "DUMMY"

                # Pick a random effect from the applicable list
                if is_player_card is True:
                    e = random.choice(BattleCard.PLAYER_CARD_EFFECTS)
                else:
                    e = random.choice(BattleCard.ENEMY_CARD_EFFECTS)

                self.effects[outcome] = e

            # Else we failed to add a new feature so off set the increment that is about to happen!!!!
            else:
                features_added -= 1

            # We think we added a new feature!
            features_added += 1

        # If we added some heal feature(s) we need to replace the placeholder with a real outcome condition...
        if len(self.heals) > 0:

            heal_value = self.heals.get("DUMMY", 0)
            del self.heals["DUMMY"]

            # If there were no blocks or hits always heal...
            if len(self.blocks) + len(self.attacks) == 0:
                outcome = Outcome.ALL
            # If these were mainly blocks...
            elif len(self.blocks) > len(self.attacks):
                # Select random blocking related outcomes
                outcome = random.choice([Outcome.ALL, Outcome.BLOCK, Outcome.BLOCK_ALL])
            # Else select hit related outcomes
            else:
                outcome = random.choice([Outcome.ALL, Outcome.HIT, Outcome.HIT_ALL])

            # Store the new heal, outcome condition and value
            self.heals[outcome] = heal_value

        # If we added an effect feature we need to replace the placeholder with a real outcome condition...
        if len(self.effects) > 0:

            outcome = "DUMMY"
            effect = self.effects.get(outcome)
            del self.effects[outcome]

            # If there were no blocks or hits always apply effect...
            if len(self.blocks) + len(self.attacks) == 0:
                outcome = Outcome.ALL
            # If these were mainly blocks...
            elif len(self.blocks) > len(self.attacks):
                # Select random blocking related outcomes
                outcome = random.choice([Outcome.ALL, Outcome.BLOCK, Outcome.BLOCK_ALL])
            # Else select hit related outcomes
            else:
                outcome = random.choice([Outcome.ALL, Outcome.HIT, Outcome.HIT_ALL])

            # Store the new effect, outcome condition and value
            self.effects[outcome] = effect


class LootCard(BaseCard):
    def __init__(self, name: str):
        super().__init__(name, CardType.LOOT)
        self.value = 1

    def __str__(self):
        text = f"Loot Card '{self.name}' value={self.value}"
        return text

    def print(self):
        print(str(self))

class CardManager:
    def __init__(self, max_hand_size: int = 1):
        self.deck = []
        self.hand = []
        self.discard = []
        self.max_hand_size = max_hand_size

    def deal_card(self, from_deck: list, to_deck: list):

        new_card = None

        if len(from_deck) > 0:
            new_card = from_deck.pop()
            to_deck.append(new_card)
        else:
            print("No cards left in the from deck")

        return new_card

    @property
    def default_hand_card(self):

        card = None

        # If no card specified just pull the top card
        if len(self.hand) > 0:
            card = self.hand[0]

        return card


    def play_card(self, selected_card: BaseCard = None):

        # If no card specified just pull the top card
        if selected_card is None and len(self.hand) > 0:
            selected_card = self.hand[0]

        if selected_card in self.hand:
            self.hand.remove(selected_card)
            self.discard.append(selected_card)
        else:
            print(f'Cant find card {selected_card} in your hand')
            selected_card = None

        return selected_card

    def replenish(self, max_hand_size: int = None):

        # What is the maximum number of cards that we can hold?
        if max_hand_size is None:
            max_hand_size = self.max_hand_size

        # Replenish hand with new cards
        while len(self.hand) < max_hand_size:

            # If deck is empty then pick up discard pile
            if len(self.deck) == 0:
                self.deck = self.discard
                self.discard = []

            self.deal_card(self.deck, self.hand)

    def remove_by_id(self, id):
        """
        Remove cards from the deck that have been tagged with a specified ID
        :param id: The id that you want to remove tagged cards
        """
        cards_to_delete = []
        for card in self.deck:
            if card.link_id == id:
                cards_to_delete.append(card)

        for card in cards_to_delete:
            self.deck.remove(card)


    def reset(self):
        self.deck = self.deck + self.discard + self.hand

    def shuffle(self):
        random.shuffle(self.deck)


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
