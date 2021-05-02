import logging
import random
from . doc_enums import *

class BaseCharacter():

    def __init__(self, name: str, type: str, is_player: bool):
        self.name = name
        self.type = type
        self.is_player = is_player
        self.health = 5
        self.max_cards_per_hand = 1
        self.effects = {}

    @property
    def is_dead(self):
        return self.health <= 0

    def print(self):
        print(f"{self.name} the {self.type} (player={self.is_player}, health={self.health}, effects={self.effects} max hand={self.max_cards_per_hand})")

    def add_effect(self, effect_name : str, tick_count : int = 3):
        self.effects[effect_name] = tick_count

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



class EnemyCharacter(BaseCharacter):
    def __init__(self, name: str, type: str):
        super().__init__(name=name, type=type, is_player=False)

class PlayerCharacter(BaseCharacter):
    def __init__(self, name: str, type: str):
        super().__init__(name=name, type=type, is_player=True)
        self.max_cards_per_hand = 3



def test():
    print(f"\nTesting {__file__}\n")

    p = PlayerCharacter("Jim", "Warrior")
    p.print()

    npc = EnemyCharacter("Egg", "Zombie")
    npc.print()


if __name__ == "__main__":
    test()
