import logging
import random
from . doc_enums import *

class BaseCharacter():

    def __init__(self, name: str, type: str, gender: str = Gender.MALE, is_player: bool = False):

        # Properties
        self.name = name
        self.type = type
        self.gender = gender
        self.is_player = is_player
        self.portrait = random.randint(0,10)

        self.effects = {}

        # Stats
        self.max_cards_per_hand = 1
        self.cards_per_hand = self.max_cards_per_hand
        self.max_health = 5
        self.health = self.max_health
        self.rounds = 0
        self.wins = 0
        self.level = 1

    @property
    def is_dead(self):
        return self.health <= 0

    @property
    def is_invincible(self):
        return Effect.INVINCIBLE in self.effects.keys()

    @property
    def is_blind(self):
        return Effect.BLIND in self.effects.keys()

    @property
    def is_confused(self):
        return Effect.CONFUSED in self.effects.keys()

    @property
    def is_sleeping(self):
        return Effect.SLEEP in self.effects.keys()


    def print(self):
        print(f"{self.name} the {self.type.value} (player={self.is_player}, health={self.health}, effects={self.effects}, max hand={self.max_cards_per_hand})")

    def level_up(self):
        self.level += 1
        self.max_health += 1

    def add_effect(self, effect_name : str, tick_count : int = 3):
        self.effects[effect_name] = tick_count

    def tick(self):

        # Process effects
        if Effect.DECAY in self.effects.keys():
            logging.info("You are rotting! Losing Health.")
            self.health -= 1
        if Effect.BURNING in self.effects.keys():
            logging.info("You are burning! Losing Health.")
            self.health -= 1
        if Effect.BLESSED in self.effects.keys():
            logging.info("You are blessed and healing")
            self.health += 1

        # Decrement effect counters
        keys_to_delete = []
        for k,v in self.effects.items():
            if v == 1:
                keys_to_delete.append(k)
                logging.info(f"Effect {k} on {self.name} wore off!")
            else:
                self.effects[k] = v - 1

        # Remove any effects that have expired
        for k in keys_to_delete:
            del self.effects[k]

    def reset(self):
        self.effects = {}
        self.health = self.max_health
        self.cards_per_hand = self.max_cards_per_hand


class EnemyCharacter(BaseCharacter):
    def __init__(self, name: str, type: str, gender: str):
        super().__init__(name=name, type=type, gender=gender, is_player=False)

class PlayerCharacter(BaseCharacter):
    def __init__(self, name: str, type: str, gender: str):
        super().__init__(name=name, type=type, gender=gender, is_player=True)
        self.max_cards_per_hand = 3
        self.cards_per_hand = self.max_cards_per_hand





def test():
    print(f"\nTesting {__file__}\n")

    p = PlayerCharacter("Jim", "Warrior")
    p.print()

    npc = EnemyCharacter("Egg", "Zombie")
    npc.print()


if __name__ == "__main__":
    test()
