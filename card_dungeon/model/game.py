from .events import *
from .battle import *
import os
from . doc_exceptions import *

class Model():

    DATA_FILES_DIR = os.path.dirname(__file__) + "\\data\\"

    # Define states to synch up with corresponding event names
    STATE_LOADED = Event.STATE_LOADED
    STATE_READY = Event.STATE_READY
    STATE_PLAYING = Event.STATE_PLAYING
    STATE_ROUND_OVER = Event.STATE_ROUND_OVER
    STATE_PAUSED = Event.STATE_PAUSED
    STATE_GAME_OVER = Event.STATE_GAME_OVER

    def __init__(self, name : str):
        # Properties
        self.name = name
        self.tick_count = 0
        self._state = None
        self._debug = False


        # Components
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

        # If we don't have a living player then create a new one
        if self.player is None or self.player.is_dead is True:
            pn = random.choice(["Keith", "Jack", "Rosie"])
            pt = random.choice(list(PlayerType))
            self.player = PlayerCharacter(name=pn, type=pt)

        # Generate a random enemy
        en = random.choice(["Edgar", "Vince","Harold"])
        et = random.choice(list(EnemyType))
        e = EnemyCharacter(name=en, type=et)

        self.battle = Battle(self.player, e)
        self.battle.initialise()

    def tick(self):
        if self.state == Model.STATE_PLAYING:
            self.tick_count += 1
        else:
            pass

    def start(self):
        self.state = Model.STATE_PLAYING
        self.player.reset()

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

        self.hacks()

        print(f"Debug={self._debug}")
        print(self)

    def hacks(self):
        for e in Effect:
            self.player.add_effect(e)

    def end(self):
        print("Ending {0}".format(__class__))

    def select_card(self, selection : int):
        print(f"Selecting card {selection}")
        if selection >0 and selection <= len(self.battle.player_cards.hand):
            self.battle.player_selected_card = self.battle.player_cards.hand[selection - 1]

    def do_round(self):

        if self.battle.player_selected_card is None:
            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.ACTION_FAILED,
                                        description="No player card selected"))
        else:
            self.battle.do_round()
            if self.battle.is_game_over:
                #self.battle.reset_round()

                # Log event if player levelled up
                if self.player.is_dead is False:
                    self.player.wins += self.player.is_dead is False
                    if self.battle.player.level <= self.battle.enemy.level:
                        self.player.level += 1
                        self.events.add_event(Event(type=Event.BATTLE,
                                                    name=Event.PLAYER_INFO,
                                                    description=f"{self.player.name} the {self.player.type.value} has gained a level!"))

                self.state = Model.STATE_GAME_OVER
            else:
                self.state = Model.STATE_ROUND_OVER

    def new_round(self):

        if self.state == Model.STATE_ROUND_OVER:
            self.state = Model.STATE_PLAYING
            self.battle.reset_round()
        else:
            print(f"Can't start a new roubnd right now!")