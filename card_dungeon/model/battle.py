import logging

from .battle_cards import *
from .characters import *


class Battle():
    def __init__(self, player: PlayerCharacter, enemy: EnemyCharacter):

        # Properties
        self.round = 0

        # Components
        self.player = player
        self.enemy = enemy

        self.player_deck = []
        self.player_hand = []
        self.player_discard = []

        self.enemy_deck = []
        self.enemy_hand = []
        self.enemy_discard = []

        self.player_selected_card = None
        self.player_round_card = None
        self.enemy_round_card = None

    @property
    def is_game_over(self):
        return self.player.is_dead or self.enemy.is_dead

    def print(self):
        print(
            f"Round {self.round}: Battle between {self.player.name} the {self.player.type} and {self.enemy.name} the {self.enemy.type}")

    def initialise(self):
        self.build_deck(10, self.player_deck)
        self.build_deck(10, self.enemy_deck)

        self.deal_card(self.player_deck, self.player_hand)
        self.deal_card(self.player_deck, self.player_hand)
        self.deal_card(self.player_deck, self.player_hand)

        self.deal_card(self.enemy_deck, self.enemy_hand)

    def start(self):

        self.deal_card(self.player_deck, self.player_hand)

    def build_deck(self, card_count: int, deck: list):
        """
        Add a specified number of randomly generated cards to a deck
        :param card_count: the number of cards that you want to add to the deck
        :param deck: the deck that you want to add the cards to
        """
        for i in range(card_count):
            new_card = BattleCard(f"Card {i}")
            new_card.generate(random.randint(1, 3))
            deck.append(new_card)

    def pick_card(self, choice : BattleCard):
            self.player_round_card = choice
            self.player_hand.remove(choice)
            self.player_discard.append(choice)

    def deal_card(self, from_deck: list, to_deck: list):

        new_card = None

        if len(from_deck) > 0:
            new_card = from_deck.pop()
            to_deck.append(new_card)
        else:
            print("No cards left in the from deck")

        return new_card

    def do_turn(self, attacker_card: BattleCard, attacker: BaseCharacter, defender_card: BattleCard,
                defender: BaseCharacter):

        print(f"\n{attacker.name} attacks {defender.name}...")
        attacker.print()
        attacker_card.print()
        defender.print()
        defender_card.print()

        turn_full_attack = True
        turn_full_defend = True

        # Attempt all of the element attacks in the attackers card
        for element, attack_count in attacker_card.attacks.items():

            # For this element, how many blocks does the defender have?
            # If attack is unblockable then 0 blocks
            block_count = defender_card.blocks.get(element, 0) * (attacker_card.is_attack_unblockable is False)

            # Calculate the damage of the attack which must not be negative
            damage = max(attack_count - block_count, 0)

            # Have we landed ALL attacks?
            turn_full_attack = turn_full_attack and (damage == attack_count)

            # Have all attacks been blocked?
            turn_full_defend = turn_full_defend and (damage == 0)

            # Print the results of the defender's block
            if block_count > 0:
                print(f"{defender.name} blocks {min(block_count, attack_count)} {element.name} attacks")

            # Print the results of the attacker's attack
            if damage > 0:
                defender.health -= damage
                print(f"{attacker.name}'s {element.name} attack does {damage} damage")

        print(f"full attack={turn_full_attack} full defend={turn_full_defend}")

    def do_round(self):

        if self.is_game_over is True:
            print("Battle is over!")
            for c in [self.player, self.enemy]:
                if c.is_dead:
                    print(f"{c.name} the {c.type} is dead!")
            return

        # Get a new card from player hand
        if self.player_selected_card is None:
            self.player_round_card = self.deal_card(self.player_hand, self.player_discard)
        else:
            self.pick_card(self.player_selected_card)

        # Get a new card from enemy's hand
        self.enemy_round_card = self.deal_card(self.enemy_hand, self.enemy_discard)

        assert self.player_round_card is not None, "The Player has not picked a card for this round"
        assert self.enemy_round_card is not None, "The Enemy has not picked a card for this round"

        # See if the player is going first...
        if self.player_round_card.is_quick is True:
            self.do_turn(self.player_round_card, self.player, self.enemy_round_card, self.enemy)
            self.do_turn(self.enemy_round_card, self.enemy, self.player_round_card, self.player)
        else:
            self.do_turn(self.enemy_round_card, self.enemy, self.player_round_card, self.player)
            self.do_turn(self.player_round_card, self.player, self.enemy_round_card, self.enemy)

        # Add any bonus or penalty to the number of cards a player is allowed in their hand
        self.player.max_cards_per_hand += self.player_round_card.new_card_count
        self.player.max_cards_per_hand -= self.enemy_round_card.new_card_count
        self.player.max_cards_per_hand = max(self.player.max_cards_per_hand, 1)

        # Heal the player if applicable
        self.player.health += self.player_round_card.heals.get(Outcome.HIT,0)

        # Heal the enemy if applicable
        self.enemy.health += self.enemy_round_card.heals.get(Outcome.HIT,0)

        # Replenish Player's hand with new cards
        while len(self.player_hand) < self.player.max_cards_per_hand:

            # If player's deck is empty then pick up discard pile
            if len(self.player_deck) == 0:
                logging.info("Picking up player's discard pile")
                self.player_deck = self.player_discard
                self.player_discard = []

            logging.info("Dealing new card to player's hand")
            self.deal_card(self.player_deck, self.player_hand)

        # Replenish Enemy's hand with new cards
        while len(self.enemy_hand) < self.enemy.max_cards_per_hand:

            # If enemy's deck is empty then pick up discard pile
            if len(self.enemy_deck) == 0:
                logging.info("Picking up enemy's discard pile")
                self.enemy_deck = self.enemy_discard
                self.enemy_discard = []

            logging.info("Dealing new card to enemy's hand")
            self.deal_card(self.enemy_deck, self.enemy_hand)

        # Reset the cards
        self.player_round_card = None
        self.enemy_round_card = None
        self.player_selected_card = None
        self.round += 1


def test():
    print(f"\nTesting {__file__}\n")

    p = PlayerCharacter(name="Keith", type="Warrior")
    npc = EnemyCharacter(name="George", type="Goblin")

    b = Battle(player=p, enemy=npc)
    b.initialise()
    b.print()

    b.start()


if __name__ == "__main__":
    test()
