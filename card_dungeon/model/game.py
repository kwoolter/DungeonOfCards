import os

from .battle import *
from .card_factory import CardFactory
from .maps import Map, Room


class Model():
    DATA_FILES_DIR = os.path.dirname(__file__) + "\\data\\"

    # Define states to synch up with corresponding event names
    STATE_LOADED = Event.STATE_LOADED
    STATE_READY = Event.STATE_READY
    STATE_PLAYING = Event.STATE_PLAYING
    STATE_ROUND_OVER = Event.STATE_ROUND_OVER
    STATE_BATTLE_OVER = Event.STATE_BATTLE_OVER
    STATE_MAP = Event.STATE_MAP_MODE
    STATE_PAUSED = Event.STATE_PAUSED
    STATE_GAME_OVER = Event.STATE_GAME_OVER

    def __init__(self, name: str):

        # Properties
        self.name = name
        self.tick_count = 0
        self._state = None
        self._debug = False

        # Components
        self.player = None
        self.battle = None
        self.events = EventQueue()
        self.loot_deck = CardManager(max_hand_size=5)
        self.dungeon_map = None

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

        self.dungeon_map = Map(self.name)
        self.dungeon_map.generate()
        self.dungeon_map.initialise()

        CardFactory.load("items.csv")

        self.new_battle()
        self.new_loot()

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

    def debug(self, debug_on: bool = None):

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

    def move(self, direction:Direction):
        self.dungeon_map.move(direction)

    def select_card(self, selection: int):
        print(f"Selecting card {selection}")
        if selection > 0 and selection <= len(self.battle.player_cards.hand):
            selected_card = self.battle.player_cards.hand[selection - 1]
            if self.battle.player_selected_card != selected_card:
                self.battle.player_selected_card = selected_card
            else:
                self.battle.player_selected_card = None

    def select_loot_card(self, selection: int):
        print(f"Selecting loot card {selection}")
        if selection > 0 and selection <= len(self.loot_deck.hand):
            selected_card = self.loot_deck.hand[selection - 1]
            if self.loot_deck.selected_card != selected_card:
                self.loot_deck.selected_card = selected_card
            else:
                self.loot_deck.selected_card = None

    def do_round(self):

        if self.battle.player_selected_card is None:
            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.ACTION_FAILED,
                                        description="No player card selected"))
        else:
            self.battle.do_round()
            self.state = Model.STATE_ROUND_OVER
            self.is_game_over()

    def is_game_over(self):

        # If battle is over...
        if self.battle.is_game_over:

            # If player survived
            if self.player.is_dead == False:

                self.player.wins += 1

                # Log event if player levelled up
                if self.battle.player.level <= self.battle.enemy.level:
                    self.player.level_up()
                    self.events.add_event(Event(type=Event.BATTLE,
                                                name=Event.PLAYER_INFO,
                                                description=f"{self.player.name} the {self.player.type.value} has gained a level!"))

                # Set state to end of the battle
                self.state = Model.STATE_BATTLE_OVER

            # Else Player died and Game Over
            else:
                self.state = Model.STATE_GAME_OVER


    def new_round(self):

        if self.state == Model.STATE_ROUND_OVER:
            self.state = Model.STATE_PLAYING
            self.battle.reset_round()
            self.is_game_over()
        else:
            print(f"Can't start a new round right now!")

    def new_loot(self):
        """
        Create a new deck of Loot Cards
        """
        for i in range(10):
            loot_name = random.choice(["Gold", "Silver", "Diamond", "Ruby", "Sapphire", "Emerald"])
            new_card = LootCard(loot_name, description=f"{loot_name} loot")
            self.loot_deck.deck.append(new_card)
        self.loot_deck.shuffle()
        self.loot_deck.replenish()
        self.loot_deck.selected_card = self.loot_deck.default_hand_card

    def new_battle(self):

        self.state = Model.STATE_LOADED

        # If we don't have a living player then create a new one
        if self.player is None or self.player.is_dead:

            pt = random.choice(list(PlayerType))
            pg = random.choice(list(Gender))
            if pg == Gender.MALE:
                pn = random.choice(["Keith", "Jack", "Monty"])
            else:
                pn = random.choice(["Jane", "Honey", "Rosie"])
            self.player = PlayerCharacter(name=pn, type=pt, gender=pg)
            self.player.print()

        # Reset the player ready for a new battle
        self.player.reset()

        # Generate a random enemy and make the same level as the player
        et = random.choice(list(EnemyType))
        eg = random.choice(list(Gender))
        if eg == Gender.MALE:
            en = random.choice(["Edgar", "Vince", "Harold", "Fred", "George", "Monty"])
        else:
            en = random.choice(["Alice", "Phoebe", "Hannah", "Elvira", "Lillith","Zora"])

        e = EnemyCharacter(name=en, type=et, gender=eg)

        # Level up the enemy and reset
        for i in range(1,self.player.level):
            e.level_up()
        e.reset()
        #e.health = 1

        # Create a new battle - player vs. enemy
        self.battle = Battle(self.player, e)
        self.battle.initialise()
