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
        self.enemy_deck = []

        self.player_selected_card = None
        self.player_round_card = None
        self.enemy_round_card = None

        self.player_cards = CardManager(max_hand_size=3)
        self.enemy_cards = CardManager(max_hand_size=1)

    @property
    def is_game_over(self):
        return self.player.is_dead or self.enemy.is_dead

    def print(self):
        print(
            f"Round {self.round}: Battle between {self.player.name} the {self.player.type} and {self.enemy.name} the {self.enemy.type}")

    def initialise(self):
        """
        Initialise the battle so that we are ready to start a round
        :rtype: object
        """

        # Build random decks for the player and the enemy
        self.build_deck(10, self.player_deck)
        self.build_deck(10, self.enemy_deck)

        self.player_cards.deck = self.player_deck
        self.enemy_cards.deck = self.enemy_deck

        self.player_cards.replenish()
        self.enemy_cards.replenish()

    def start(self):
        pass


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

    def do_attack(self, attacker_card: BattleCard, attacker: BaseCharacter, defender_card: BattleCard,
                  defender: BaseCharacter):
        """
        Perform an attack on a defender using teh specified attack and defend cards
        :param attacker_card: The card that the attacker is going to use
        :param attacker: The attacker
        :param defender_card: The card that the defender is going to use
        :param defender: The defender
        """
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
        """
        Do a round in the battle
        :return:
        """
        if self.is_game_over is True:
            print("Battle is over!")
            for c in [self.player, self.enemy]:
                if c.is_dead:
                    print(f"{c.name} the {c.type} is dead!")
            return

        # Get a new card from player's hand
        self.player_round_card = self.player_cards.play_card(self.player_selected_card)

        # Get a new card from enemy's hand
        self.enemy_round_card = self.enemy_cards.play_card()

        assert self.player_round_card is not None, "The Player has not picked a card for this round"
        assert self.enemy_round_card is not None, "The Enemy has not picked a card for this round"

        # See if the player is going first...
        if self.player_round_card.is_quick is True:
            self.do_attack(self.player_round_card, self.player, self.enemy_round_card, self.enemy)
            self.do_attack(self.enemy_round_card, self.enemy, self.player_round_card, self.player)
        # Else the enemy goes first
        else:
            self.do_attack(self.enemy_round_card, self.enemy, self.player_round_card, self.player)
            self.do_attack(self.player_round_card, self.player, self.enemy_round_card, self.enemy)

        # Add any bonus or penalty to the number of cards a player is allowed in their hand
        self.player.max_cards_per_hand += self.player_round_card.new_card_count
        self.player.max_cards_per_hand -= self.enemy_round_card.new_card_count
        self.player.max_cards_per_hand = max(self.player.max_cards_per_hand, 1)


        # Heal the player if applicable
        self.player.health += self.player_round_card.heals.get(Outcome.HIT,0)

        # Heal the enemy if applicable
        self.enemy.health += self.enemy_round_card.heals.get(Outcome.HIT,0)

        # Replenish Player's hand with new cards
        self.player_cards.replenish()

        # Discard cards from the player's hand
        for i in range(self.enemy_round_card.new_card_count):
            self.player_cards.play_card()

        # Replenish Enemy's hand with new cards
        self.enemy_cards.replenish()

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
