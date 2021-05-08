from .events import *
from .battle import *
import os

class Model():

    DATA_FILES_DIR = os.path.dirname(__file__) + "\\data\\"

    # Define states to synch up with corresponding event names
    STATE_LOADED = Event.STATE_LOADED
    STATE_READY = Event.STATE_READY
    STATE_PLAYING = Event.STATE_PLAYING
    STATE_PAUSED = Event.STATE_PAUSED
    STATE_GAME_OVER = Event.STATE_GAME_OVER

    def __init__(self, name : str):
        # Properties
        self.name = name
        self.tick_count = 0
        self._state = None
        self._debug = False

        # Model Components
        self.player = None
        self.battle = None
        self.events = EventQueue()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if new_state != self._state:
            self._old_state = self._state
            self._state = new_state
            self.events.add_event(Event(type=Event.STATE,
                                        name=self.state,
                                        description="Game state changed to {0}".format(self.state)))

    def initialise(self):
        self.state = Model.STATE_LOADED

        p = PlayerCharacter(name="Keith", type="Warrior")
        self.player = p

        en = random.choice(["Edgar", "Vince","Harold"])
        et = random.choice(["Rat", "Spider", "Ghost"])
        e = EnemyCharacter(name=en, type=et)

        self.battle = Battle(p, e)
        self.battle.initialise()

    def tick(self):
        if self.state == Model.STATE_PLAYING:
            self.tick_count += 1
        else:
            pass

    def start(self):
        self.state = Model.STATE_PLAYING

    def pause(self, pause_on=None):

        if pause_on is True:
            self.state = Model.STATE_PAUSED
        elif pause_on is False and self.state == Model.STATE_PAUSED:
            self.state = Model.STATE_PLAYING
        elif pause_on is None:
            if self.state == Model.STATE_PAUSED:
                self.state = Model.STATE_PLAYING
            elif self.state == Model.STATE_PLAYING:
                self.state = Model.STATE_PAUSED

    def process_event(self, new_event):
        print("Default Game event process:{0}".format(new_event))

        if new_event.type == Event.DEBUG:
            self.debug()

    def debug(self, debug_on : bool = None):

        if debug_on is None:
            self._debug = not self._debug
        else:
            self._debug = debug_on

        print(f"Debug={self._debug}")

    def end(self):
        print("Ending {0}".format(__class__))


    def select_card(self, selection : int):
        print(f"Selecting card {selection}")
        if selection >0 and selection <= len(self.battle.player_cards.hand):
            self.battle.player_selected_card = self.battle.player_cards.hand[selection - 1]

    def do_round(self):
        self.battle.do_round()