from .characters import *
from .battle_cards import *

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



    def print(self):
        print(f"Round {self.round}: Battle between {self.player.name} the {self.player.type} and {self.enemy.name} the {self.enemy.type}")

    def initialise(self):
        self.deal(10, self.player_deck)
        self.deal(10,self.enemy_deck)

    def deal(self, card_count : int, deck : list):

        for i in range(card_count):
            pass



def test():
    print(f"\nTesting {__file__}\n")

    p = PlayerCharacter(name = "Keith", type = "Warrior")
    npc = EnemyCharacter(name = "George", type = "Goblin")

    b = Battle(player=p, enemy=npc)
    b.initialise()
    b.print()

if __name__ == "__main__":
    test()
