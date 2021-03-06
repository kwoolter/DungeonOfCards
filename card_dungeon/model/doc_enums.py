from enum import Enum, auto

class Effect(Enum):
    BLIND = "Blinded"
    CONFUSED = "Confused"
    DECAY = "Decaying"
    BURNING = "Burning"
    INVINCIBLE = "Invincible"
    BLESSED = "Blessed"
    SLEEP = "Sleeping"

class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"

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

class CharacterFeature(Enum):
    HEALTH = "Health"
    LEVEL = "Level"

class CharacterSlot(Enum):
    HEAD = "Head"
    BODY = "Body"
    MAIN_HAND = "Main Hand"
    OFF_HAND= "Off Hand"
    NONE = "None"

class CardFeature(Enum):
    ATTACK_MELEE = "Melee Attack"
    ATTACK_MAGIC = "Magic Attack"
    BLOCK_MELEE = "Melee Block "
    BLOCK_MAGIC = "Magic Block"
    QUICK = "Quick"
    HEAL = "Heal"
    DRAIN = "Drain"
    DEAL = "Extra Card"
    UNBLOCKABLE = "Unblockable"
    EFFECT = "Effect"

class Loot(Enum):
    TOKEN = "Token"

class Outcome(Enum):
    ALL = "always"
    HIT = "a hit"
    HIT_ALL = "all hits"
    BLOCK = "a block"
    BLOCK_ALL = "all blocks"
    NEVER = "never"

class CardType(Enum):
    BATTLE = 1
    LOOT = 2
    MAP = 3

def enum_value_to_key(enum_class:Enum, value:str, default = None):
    result = default
    try:
        result = enum_class._value2member_map_[value]
    except:
        pass
    return result