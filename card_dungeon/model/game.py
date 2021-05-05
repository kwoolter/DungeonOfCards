from .events import *
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

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if new_state != self._state:
            self._old_state = self._state
            self._state = new_state

    def initialise(self):
        pass

    def tick(self):
        pass

    def end(self):
        print("Ending {0}".format(__class__))
