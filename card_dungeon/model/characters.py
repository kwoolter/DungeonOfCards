class BaseCharacter():

    def __init__(self, name: str, type: str, is_player: bool):
        self.name = name
        self.type = type
        self.is_player = is_player
        self.health = 5
        self.max_cards_per_hand = 1

    @property
    def is_dead(self):
        return self.health <= 0

    def print(self):
        print(f"{self.name} the {self.type} (player={self.is_player}, health={self.health}, max hand={self.max_cards_per_hand})")


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
