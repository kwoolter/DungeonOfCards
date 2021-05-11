import collections


class Event():
    # Event Types
    DEBUG = "debug"
    QUIT = "quit"
    DEFAULT = "default"
    STATE = "state"
    GAME = "game"
    BATTLE = "Battle"
    WORLD = "world"
    EFFECT = "effect"

    # Define states
    STATE_LOADED = "Game Loaded"
    STATE_READY = "Game Ready"
    STATE_PLAYING = "Game Playing"
    STATE_ROUND_OVER = "Battle Round Over"
    STATE_PAUSED = "Game Paused"
    STATE_GAME_OVER = "Game Over"

    # Event Names
    TICK = "Tick"
    EFFECT_START = "Effect Start"
    EFFECT_END = "Effect End"
    PLAYER_INFO = "Player Info"
    ENEMY_INFO = "Enemy Info"
    BATTLE_ROUND_OVER = "Battle Round Over"
    ACTION_INFO = "Action Info"
    ACTION_FAILED = "action failed"
    ACTION_SUCCEEDED = "action succeeded"
    HELP = "Help"

    # Effects
    EFFECT_MELEE_ATTACK = "Melee Attack"

    EFFECT_DURATION = {
        EFFECT_MELEE_ATTACK: 20
    }

    def __init__(self, name: str, description: str = None, type: str = DEFAULT):
        self.name = name
        self.description = description
        self.type = type

    def __str__(self):
        return "{0}:{1} ({2})".format(self.name, self.description, self.type)


class EventQueue():
    def __init__(self):
        self.events = collections.deque()

    def add_event(self, new_event: Event):
        self.events.append(new_event)

    def get_next_event(self):
        next_event = None
        if len(self.events) > 0:
            next_event = self.events.pop()
        return next_event

    def clear(self):
        self.events.clear()

    def size(self):
        return len(self.events)

    def print(self):
        for event in self.events:
            print(event)
