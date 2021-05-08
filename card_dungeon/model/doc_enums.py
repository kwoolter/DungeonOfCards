from enum import Enum, auto

class Effect(Enum):
    BLIND = "Blinded"
    CONFUSED = "Confused"
    DECAY = "Decaying"
    BURNING = "Burning"
    INVINCIBLE = "Invincible"
    BLESSED = "Blessed"
    SLEEP = "Sleeping"

class PlayerType(Enum):
    WARRIOR = "Warrior"
    CHUMP = "Chump"
    BARBARIAN = "Barbarian"

class EnemyType(Enum):
    RAT = "Rat"
    GOBLIN = "Goblin"
    GHOST = "Ghost"
    MIMIC = "Mimic"
    SCORPION = "Scorpion"
    PIGGY = "Wild Piggy"
    RATMAN = "Rat Man"
    SNAKE = "Snake"
    BUNNY = "Angry Bunny"


class CardFeature(Enum):
    ATTACK_MELEE = "Melee Attack"
    ATTACK_MAGIC = "Magic Attack"
    BLOCK_MELEE = "Melee Block "
    BLOCK_MAGIC = "Magic Block"
    QUICK = "Quick"
    HEAL = "Heal"
    DEAL = "Extra Card"
    UNBLOCKABLE = "Unblockable"
    EFFECT = "Effect"

class Loot(Enum):
    TOKEN = "Token"


# Types of attack and block elements
class Element(Enum):
    PHYSICAL = auto()
    MAGICAL = auto()
    # FIRE = 1
    # ICE = 2
    # WATER = 3

class Outcome(Enum):
    ALL = "always"
    HIT = "a hit"
    HIT_ALL = "all hits"
    BLOCK = "a block"
    BLOCK_ALL = "all blocks"

class CardType(Enum):
    BATTLE = 1
    LOOT = 2
    MAP = 3
