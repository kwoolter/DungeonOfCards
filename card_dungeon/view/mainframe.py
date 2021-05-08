import pygame
import os
import card_dungeon.model as model
from . view import *
from . graphics import *
from . card_views import *
from . character_view import *

class MainFrame(View):

    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    TRANSPARENT = (0, 255, 0)

    def __init__(self, model: model.Model):

        super().__init__()

        self._debug = False

        self.model = model
        self.surface = None
        self.width = 600
        self.height = 600
        self._debug = False

        self.battle_card_view_player = None
        self.battle_card_view_enemy = None

        self.player_view = None
        self.enemy_view = None


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

        self.player_view = CharacterView(width=200,height=200)
        self.player_view.initialise(self.model.battle.player)
        self.player_view.bg = Colours.DARK_BLUE

        self.enemy_view = CharacterView(width=200, height=200)
        self.enemy_view.initialise(self.model.battle.enemy)
        self.enemy_view.bg = Colours.DARK_RED


        self.battle_card_view_player = BattleCardView(width=200, height=160)
        c = model.BattleCard("Player Card")
        c.generate(5, is_player_card=True)
        self.battle_card_view_player.initialise(c)
        self.battle_card_view_player.bg = Colours.DARK_BLUE


        self.battle_card_view_enemy = BattleCardView(width=200, height=160)
        c = model.BattleCard("Enemy Card")
        c.generate(5, is_player_card=False)
        self.battle_card_view_enemy.initialise(c)
        self.battle_card_view_enemy.bg = Colours.DARK_RED

    def print(self):

        print("Printing DoC view...")

    def draw(self):

        pane_rect = self.surface.get_rect()
        self.surface.fill(Colours.WHITE)

        grid_size = 34
        for x in range(pane_rect.x, pane_rect.width, grid_size):
            # line(surface, color, start_pos, end_pos, width)
            pygame.draw.line(self.surface,Colours.CYAN, (x,pane_rect.top),(x,pane_rect.bottom), 2)

        for y in range(pane_rect.top, pane_rect.bottom, grid_size):
            pygame.draw.line(self.surface, Colours.CYAN, (pane_rect.left, y), (pane_rect.right,y))

        padding = 4
        x = padding
        y = padding

        # Draw the player's information
        self.player_view.draw()
        self.surface.blit(self.player_view.surface, (x,y))

        # Draw the enemy's information
        self.enemy_view.draw()
        pane_rect = self.enemy_view.surface.get_rect()
        pane_rect.right = self.surface.get_rect().right - padding
        pane_rect.y = padding
        self.surface.blit(self.enemy_view.surface, pane_rect)


        y = pane_rect.bottom + 20
        x = padding

        # Draw all of the cards in the player's hand
        for card in self.model.battle.player_cards.hand:

            cv = BattleCardView(width=200, height=160)
            cv.initialise(card)

            cv.is_highlighted = card == self.model.battle.player_selected_card
            cv.is_concealed = self.model.player.is_confused

            cv.fg = Colours.DARK_BLUE
            cv.draw()
            self.surface.blit(cv.surface, (x, y))
            y+= 60
            x+= 8

        y = pane_rect.bottom + 20

        # Draw all of the cards in the enemy's hand
        for card in self.model.battle.enemy_cards.hand:
            cv = BattleCardView(width=200, height=160)
            cv.initialise(card)
            cv.fg = Colours.DARK_RED

            cv.is_concealed = self.model.player.is_blind

            cv.draw()
            pane_rect = self.battle_card_view_enemy.surface.get_rect()
            pane_rect.right = self.surface.get_rect().right - padding
            pane_rect.y = y
            self.surface.blit(cv.surface, pane_rect)
            y+= 60
            x+= 8

        # Draw game state msg box if not playing
        if self.model.state != model.Model.STATE_PLAYING:
            pane_rect = self.surface.get_rect()

            msg_box_width = 200
            msg_box_height = 64
            msg_rect = pygame.Rect((pane_rect.width - msg_box_width) / 2,
                                   (pane_rect.height - msg_box_height) / 2, msg_box_width, msg_box_height)

            pygame.draw.rect(self.surface,
                             Colours.DARK_GREY,
                             msg_rect,
                             0)

            pygame.draw.rect(self.surface,
                             Colours.LIGHT_GREY,
                             msg_rect,
                             2)

            draw_text(surface=self.surface,
                      msg="{0}".format(self.model.state),
                      x=pane_rect.width / 2,
                      y=pane_rect.height / 2,
                      size=32,
                      centre=True,
                      fg_colour=Colours.LIGHT_GREY,
                      bg_colour=Colours.DARK_GREY)


    def update(self):
        pygame.display.update()

    def end(self):
        pygame.quit()
        print("Ending {0}".format(__class__))

    def tick(self):

        super().tick()


    def process_event(self, new_event: model.Event):

        super().process_event(new_event)

