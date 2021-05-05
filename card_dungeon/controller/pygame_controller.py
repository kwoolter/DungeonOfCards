import card_dungeon.model as model
import card_dungeon.view as view

import os
import pygame
from pygame.locals import *


class DoCGUIController:

    def __init__(self):
        self.m = model.Model("Dungeon of Cards")
        self.v = view.MainFrame(self.m)

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

        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, USEREVENT])

        loop = True

        while loop is True:


            # If we are playing the game then process all of the key controls
            if self.m.state == model.Model.STATE_PLAYING:
                # Key pressed events - more time critical actions
                keys = pygame.key.get_pressed()

            # Loop to process pygame events
            for event in pygame.event.get():

                if self.m.state == model.Model.STATE_PLAYING:

                    # Timer events for the model to process
                    if event.type == USEREVENT + 1:
                        self.m.tick()

                    # Timer for the view time based events
                    elif event.type == USEREVENT + 2:
                        self.v.tick()


                    # Key UP events - less time critical actions
                    elif event.type == KEYUP:
                        pass

                    # Key DOWN events - less time critical actions
                    elif event.type == KEYDOWN:
                        pass

                # Process events for when the game is in state LOADED
                elif self.m.state == model.Model.STATE_LOADED:

                    # Key events
                    if event.type == KEYUP:
                        # Space to start the game
                        if event.key == K_SPACE:
                            pass
                    # Timer events
                    elif event.type == USEREVENT + 2:
                        self.v.tick()

                    # Timer for talking
                    elif event.type == USEREVENT + 3:
                        self.m.talk_to_npc(npc_object=None, npc_name="The Master", world_id=self.m.state)

                # Process events for when the game is in state READY
                elif self.m.state == model.Model.STATE_READY:

                    # Key events
                    if event.type == KEYUP:
                        # Space to start the game
                        if event.key == K_SPACE:
                            self.m.start()
                        elif event.key == K_F2:
                            self.audio.change_volume()
                        elif event.key == K_F3:
                            self.audio.change_volume(-0.1)
                        # Debug print game status info
                        elif event.key == K_F12 and self._debug is True:
                            self.v.print()
                            self.m.print()
                            self.audio.print()
                    # Timer events
                    elif event.type == USEREVENT + 2:
                        self.v.tick()

                    # Timer for talking
                    elif event.type == USEREVENT + 3:
                        pass


                # Quit event
                if event.type == QUIT:
                    loop = False

            self.v.draw()
            self.v.update()

            FPSCLOCK.tick(60)

        self.end()