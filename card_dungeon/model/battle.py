from .characters import *
from .battle_cards import *
import logging

class Battle():
    def __init__(self, player : PlayerCharacter, enemy : EnemyCharacter):

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

        self.player_round_card = None
        self.enemy_round_card = None



    def print(self):
        print(f"Round {self.round}: Battle between {self.player.name} the {self.player.type} and {self.enemy.name} the {self.enemy.type}")

    def initialise(self):
        self.build_deck(10, self.player_deck)
        self.build_deck(10, self.enemy_deck)

        for i in range(3):
            self.deal_card(self.player_deck, self.player_hand)

    def start(self):

        self.do_round()

    def build_deck(self, card_count : int, deck : list):

        for i in range(card_count):
            new_card = BattleCard(f"Card {i}")
            new_card.generate(random.randint(1,3))
            deck.append(new_card)

    def deal_card(self, from_deck : list, to_deck : list):
        new_card = from_deck.pop()
        to_deck.append(new_card)

    def do_turn(self, card : BattleCard, attacker : BaseCharacter, defender : BaseCharacter ):
        attacker.print()
        defender.print()
        card.print()

    def do_round(self):

        if len(self.player_hand) == 0:
            if len(self.player_deck) == 0:
                logging.info("Picking up player's discard pile")
                self.player_deck = self.player_discard
                self.player_discard = []

            logging.info("Dealling new cards to player's hand")
            self.deal_card(self.player_deck, self.player_hand, 3)

        self.player_round_card = self.player_hand.pop()

        if len(self.enemy_deck) == 0:
            self.enemy_deck = self.enemy_discard
            self.enemy_discard = 0


        self.enemy_round_card = self.enemy_deck.pop()

        assert self.player_round_card is not None, "The Player has not picked a card for this round"
        assert self.enemy_round_card is not None, "The Enemy has not picked a card for this round"


        # See if the player is going first...
        if self.player_round_card.is_quick is True:
            self.do_turn(self.player_round_card, self.player, self.enemy)
            self.do_turn(self.enemy_round_card, self.enemy, self.player)
        else:
            self.do_turn(self.enemy_round_card, self.enemy, self.player)
            self.do_turn(self.player_round_card, self.player, self.enemy)

        # Reset the cards
        self.player_found_card = None
        self.enemy_round_card = None
        self.round += 1

def test():
    print(f"\nTesting {__file__}\n")

    p = PlayerCharacter(name = "Keith", type = "Warrior")
    npc = EnemyCharacter(name = "George", type = "Goblin")

    b = Battle(player=p, enemy=npc)
    b.initialise()
    b.print()

    b.start()

if __name__ == "__main__":
    test()
