import card_dungeon.model as model
import card_dungeon.view as view

import os
import pygame
from pygame.locals import *


class DoCGUIController:

    def __init__(self):
        self.m = model.Model("Dungeon of Cards")
        self.v = view.MainFrame(self.m)
        self.events = self.m.events

        self._debug = False

    def initialise(self):

        pygame.init()

        self.m.initialise()
        self.v.initialise()

    def debug(self):
        self._debug = not self._debug
        self.m.events.add_event(model.Event(type=model.Event.DEBUG,
                                            name="Debug={0}".format(self._debug),
                                            description="Debug mode = {0}".format(self._debug)))
        if self._debug is True:
            print("\n\nDEBUG MODE\n\n")

    def end(self):
        self.m.end()
        self.v.end()

    def run(self):

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        FPSCLOCK = pygame.time.Clock()

        # Model tick timer
        pygame.time.set_timer(USEREVENT + 1, 15)

        # View tick timer
        pygame.time.set_timer(USEREVENT + 2, 300)

        # Sound effects tick timer
        pygame.time.set_timer(USEREVENT + 3, 8000)

        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONUP, USEREVENT])

        loop = True

        while loop is True:

            # Loop to process game events
            event = self.events.get_next_event()
            while event is not None:

                try:
                    self.m.process_event(event)
                    self.v.process_event(event)

                except Exception as err:
                    print("Caught exception {0}".format(str(err)))

                if event.type == model.Event.QUIT:
                    loop = False
                    break

                event = self.events.get_next_event()

            # If we are playing the game then process all of the key controls
            if self.m.state == model.Model.STATE_PLAYING:
                # Key pressed events - more time critical actions
                keys = pygame.key.get_pressed()

            # Loop to process pygame events
            for event in pygame.event.get():

                # See what actions have been performed...
                actions = self.handle_state_events(event)

                # Process events for when the game is in state PLAYING
                if self.m.state == model.Model.STATE_PLAYING:

                    # Timer events for the model to process
                    if event.type == USEREVENT + 1:
                        self.m.tick()

                    # Timer for the view time based events
                    elif event.type == USEREVENT + 2:
                        self.v.tick()

                    else:
                        if actions.get("PAUSE"):
                            self.m.pause()
                        elif actions.get("GO"):
                            self.v.batte_round_view.initialise(self.m.battle)
                            self.m.do_round()

                        n = actions.get("SELECT", 0)
                        if n > 0:
                            self.m.select_card(n)


                # Process events for when the game is in state PLAYING
                elif self.m.state == model.Model.STATE_ROUND_OVER:
                    if actions.get("CONTINUE"):
                        self.m.new_round()

                # Process events for when the game is in state PLAYING
                elif self.m.state == model.Model.STATE_BATTLE_OVER:
                    if actions.get("GO"):
                        card = self.m.loot_deck.selected_card
                        if card is not None:
                            print(f"You chose card {card}")
                            self.m.new_battle()
                            self.v.initialise()

                    n = actions.get("SELECT", 0)
                    if n > 0:
                        self.m.loot_deck.select_card(n)

                # Process events for when the game is in MAP mode
                elif self.m.state == model.Model.STATE_MAP:
                    if actions.get("GO"):
                        self.m.state = model.Model.STATE_PLAYING
                    else:
                        direction = actions.get("MOVE", None)
                        if direction is not None:
                            self.m.move(direction)

                # Process events for when the game is in state LOADED
                elif self.m.state == model.Model.STATE_LOADED:
                    if actions.get("CONTINUE"):
                        self.m.start()
                        self.m.state = model.Model.STATE_MAP
                    elif actions.get("TEST"):
                        self.m.player = None
                        self.m.new_battle()
                        self.v.initialise()

                    # Timer events
                    if event.type == USEREVENT + 2:
                        self.v.tick()

                    # Timer for talking
                    elif event.type == USEREVENT + 3:
                        pass

                # Process events for when the game is in state READY
                elif self.m.state == model.Model.STATE_READY:
                    if actions.get("CONTINUE"):
                        self.m.start()

                    # Timer events
                    if event.type == USEREVENT + 2:
                        self.v.tick()
                    # Timer for talking
                    elif event.type == USEREVENT + 3:
                        pass

                # Process events for when the game is in state PAUSED
                elif self.m.state == model.Model.STATE_PAUSED:
                    if actions.get("PAUSE"):
                        self.m.pause()
                    elif actions.get("DEBUG"):
                        self.m.debug()
                        self.v.print()
                    elif actions.get("QUIT"):
                        loop = False

                # Process events for when the game is in state GAME OVER
                elif self.m.state == model.Model.STATE_GAME_OVER:
                    if actions.get("CONTINUE"):
                        self.m.new_battle()
                        self.v.initialise()

                # Quit event
                if event.type == QUIT:
                    loop = False

            self.v.draw()
            self.v.update()

            FPSCLOCK.tick(20)

        self.end()

    def handle_state_events(self, event):
        actions = {}

        # Generic Key events
        if event.type == KEYUP:
            # SPACE = Continue
            if event.key == K_SPACE:
                actions["CONTINUE"] = True
        # Generic Mouse events - MOUSEBUTTONUP
        elif event.type == pygame.MOUSEBUTTONUP:
            actions["CONTINUE"] = True

        if self.m.state == model.Model.STATE_PLAYING:
            actions.update(self.handle_state_events_PLAYING(event))
        elif self.m.state == model.Model.STATE_LOADED:
            actions.update(self.handle_state_events_LOADED(event))
        elif self.m.state == model.Model.STATE_ROUND_OVER:
            actions.update(self.handle_state_events_ROUND_OVER(event))
        elif self.m.state == model.Model.STATE_BATTLE_OVER:
            actions = {}
            actions.update(self.handle_state_events_BATTLE_OVER(event))
        elif self.m.state == model.Model.STATE_GAME_OVER:
            actions.update(self.handle_state_events_GAME_OVER(event))
        if self.m.state == model.Model.STATE_MAP:
            actions.update(self.handle_state_events_MAP_MODE(event))
        elif self.m.state == model.Model.STATE_PAUSED:
            actions.update(self.handle_state_events_PAUSED(event))

        return actions


    def handle_state_events_BATTLE_OVER(self, event):
        actions = {}

        # Key events
        if event.type == KEYUP:
            # Pick a card to play
            if event.key >= K_1 and event.key <= K_9:
                n = event.key - K_1 + 1
                actions["SELECT"] = n
            # Go and play!
            elif event.key == K_RETURN:
                actions["GO"] = True

        # handle MOUSEBUTTONUP
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            # Get the name of the zone that the user clicked on
            zone = self.v.on_click(pos)

            # If it was a recognizable zone...
            if zone is not None:
                if zone == "Choose Button":
                    actions["GO"] = True
                elif zone.startswith("Loot Card"):
                    n = int(zone.split(":")[1])
                    actions["SELECT"] = n
                else:
                    print(f"Nothing happened when you clicked on zone '{zone}' in state {self.m.state}")

        return actions

    def handle_state_events_GAME_OVER(self, event):
        actions = {}

        # Key events
        if event.type == KEYUP:
            # Re-initialise the game
            if event.key == K_F5:
                actions["TEST"] = True

        return actions

    def handle_state_events_LOADED(self, event):
        actions = {}

        # Key events
        if event.type == KEYUP:
            # Re-initialise the game
            if event.key == K_F5:
                actions["TEST"] = True

        return actions

    def handle_state_events_ROUND_OVER(self, event):
        actions = {}

        # Key events
        if event.type == KEYUP:
            # Re-initialise the game
            if event.key == K_F5:
                actions["TEST"] = True

        return actions

    def handle_state_events_PAUSED(self, event):
        actions = {}

        # Key events
        if event.type == KEYUP:
            # Escape to Un-pause
            if event.key == K_ESCAPE:
                actions["PAUSE"] = True
            # F4 to quit
            elif event.key == K_F4:
                actions["QUIT"] = True
            # F12 to toggle debug
            elif event.key == K_F12:
                actions["DEBUG"] = True
        # Mouse events - MOUSEBUTTONUP to unpause
        elif event.type == pygame.MOUSEBUTTONUP:
            actions["PAUSE"] = True

        return actions

    def handle_state_events_PLAYING(self, event):
        actions = {}

        # Key events
        if event.type == KEYUP:
            # Re-initialise the game
            if event.key == K_F5:
                actions["TEST"] = True
            elif event.key == K_ESCAPE:
                actions["PAUSE"] = True
            # Pick a card to play
            elif event.key >= K_1 and event.key <= K_9:
                n = event.key - K_1 + 1
                actions["SELECT"] = n
            # Go and play!
            elif event.key == K_RETURN:
                actions["GO"] = True

        # handle MOUSEBUTTONUP
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            # Get the name of the zone that the user clicked on
            zone = self.v.on_click(pos)

            # If it was a recognisable zone...
            if zone is not None:
                if zone == "Play Button":
                    actions["GO"] = True
                elif zone.startswith("Player Card"):
                    n = int(zone.split(":")[1])
                    actions["SELECT"] = n
                else:
                    print(f"Nothing happened when you clicked on zone '{zone}' in state {self.m.state}")

        return actions


    def handle_state_events_MAP_MODE(self, event):
        actions = {}

        # Key events
        if event.type == KEYUP:
            # Move selected Room
            if event.key == K_UP:
                actions["MOVE"] = model.Direction.NORTH
            elif event.key == K_DOWN:
                actions["MOVE"] = model.Direction.SOUTH
            elif event.key == K_LEFT:
                actions["MOVE"] = model.Direction.WEST
            elif event.key == K_RIGHT:
                actions["MOVE"] = model.Direction.EAST
            # Go and play!
            elif event.key == K_RETURN:
                actions["GO"] = True

        return actions
