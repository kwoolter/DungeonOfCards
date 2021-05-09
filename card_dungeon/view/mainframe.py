import pygame
import os
import card_dungeon.model as model
from .view import *
from .graphics import *
from .card_views import BattleCardView
from .character_view import CharacterView
from . battle_views import BattleRoundView
from .game_image_manager import *


class MainFrame(View):
    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    TRANSPARENT = (0, 255, 0)

    def __init__(self, model: model.Model):

        super().__init__()

        self._debug = False

        im = DoCImageManager()
        im.initialise()
        View.IMAGE_MANAGER = im

        self.model = model
        self.surface = None
        self.width = 1000
        self.height = 600

        self.card_width = 150
        self.card_height = 180

        self._debug = False

        self.battle_card_view_player = None
        self.battle_card_view_enemy = None

        self.player_view = None
        self.enemy_view = None

        self.batte_round_view = None

    def initialise(self):

        super().initialise()

        print("Initialising {0}".format(__class__))

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption(self.model.name)

        self.surface = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWACCEL)

        filename = MainFrame.RESOURCES_DIR + "icon.png"

        try:
            image = pygame.image.load(filename)
            image = pygame.transform.scale(image, (32, 32))
            pygame.display.set_icon(image)
        except Exception as err:
            print(str(err))


        self.batte_round_view = BattleRoundView(width=600, height=240)
        self.batte_round_view.initialise(self.model.battle)

        self.player_view = CharacterView(width=200, height=240)
        self.player_view.initialise(self.model.battle.player)
        self.player_view.fg = Colours.BLUE

        self.enemy_view = CharacterView(width=200, height=240)
        self.enemy_view.initialise(self.model.battle.enemy)
        self.enemy_view.fg = Colours.RED


    def print(self):

        print("Printing DoC view...")

    def draw(self):

        pane_rect = self.surface.get_rect()
        self.surface.fill(Colours.WHITE)

        grid_size = 34
        grid_colour = (190, 244, 255)

        for x in range(pane_rect.x, pane_rect.width, grid_size):
            pygame.draw.line(self.surface, grid_colour, (x, pane_rect.top), (x, pane_rect.bottom), 2)

        for y in range(pane_rect.top, pane_rect.bottom, grid_size):
            pygame.draw.line(self.surface, grid_colour, (pane_rect.left, y), (pane_rect.right, y), 2)

        padding = 4
        x = padding
        y = padding

        # Draw the player's information
        self.player_view.draw()
        self.surface.blit(self.player_view.surface, (x, y))

        # Draw the enemy's information
        self.enemy_view.draw()
        pane_rect = self.enemy_view.surface.get_rect()
        pane_rect.right = self.surface.get_rect().right - padding
        pane_rect.y = padding
        self.surface.blit(self.enemy_view.surface, pane_rect)

        y = pane_rect.bottom + 10
        x = padding

        # Draw all of the cards in the player's hand
        for i, card in enumerate(self.model.battle.player_cards.hand):

            cv = BattleCardView(width=self.card_width, height=self.card_height)
            cv.initialise(card)

            cv.is_highlighted = card == self.model.battle.player_selected_card
            cv.is_concealed = self.model.player.is_confused

            cv.fg = Colours.BLUE
            cv.draw()
            self.surface.blit(cv.surface, (x, y))

            # Draw the number below the card
            fg = Colours.WHITE
            bg = Colours.BLUE

            if card == self.model.battle.player_selected_card:
                bg = Colours.GOLD

            draw_text(self.surface,
                      f" {i + 1} ",
                      x + int(cv.width / 2),
                      y + cv.height,
                      64,
                      fg_colour=fg,
                      bg_colour=bg)

            y += 0
            x += cv.width + padding

        y = pane_rect.bottom + 10

        # Draw all of the cards in the enemy's hand
        for card in self.model.battle.enemy_cards.hand:
            cv = BattleCardView(width=self.card_width, height=self.card_height)
            cv.initialise(card)
            cv.fg = Colours.RED

            cv.is_concealed = self.model.player.is_blind

            cv.draw()
            view_rect = cv.surface.get_rect()
            view_rect.right = self.surface.get_rect().right - padding
            view_rect.y = y
            self.surface.blit(cv.surface, view_rect)
            y += 60
            x += 8

        # Draw the battle
        pane_rect = self.surface.get_rect()
        self.batte_round_view.draw()
        view_rect = self.batte_round_view.surface.get_rect()
        view_rect.centerx = pane_rect.centerx
        view_rect.y = padding
        self.surface.blit(self.batte_round_view.surface, view_rect)


        # Draw game state msg box if not playing
        if self.model.state != model.Model.STATE_PLAYING:
            pane_rect = self.surface.get_rect()

            msg_box_width = 350
            msg_box_height = 100
            msg_rect = pygame.Rect(0, 0, msg_box_width, msg_box_height)
            bg = grid_colour

            msg_rect.center = pane_rect.center

            pygame.draw.rect(self.surface,
                             bg,
                             msg_rect,
                             0)

            pygame.draw.rect(self.surface,
                             Colours.GREY,
                             msg_rect,
                             4)

            draw_text(surface=self.surface,
                      msg="{0}".format(self.model.state),
                      x=pane_rect.width / 2,
                      y=pane_rect.height / 2,
                      size=40,
                      centre=True,
                      fg_colour=Colours.GREY,
                      bg_colour=bg)

    def update(self):
        pygame.display.update()

    def end(self):
        pygame.quit()
        print("Ending {0}".format(__class__))

    def tick(self):

        super().tick()

    def process_event(self, new_event: model.Event):

        super().process_event(new_event)
