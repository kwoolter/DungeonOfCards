import pygame
import os
import card_dungeon.model as model
from . view import *
from . graphics import *
from . card_views import *

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

        self.battle_card_view = None


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


        self.battle_card_view = BattleCardView(width=140, height=160)
        c = model.BattleCard("Card1")
        c.generate(5)
        self.battle_card_view.initialise(c)

    def print(self):

        print("Printing Dark Work view...")



    def draw(self):

        pane_rect = self.surface.get_rect()

        x = 0
        y = 0

        self.surface.fill(Colours.RED)

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

        self.battle_card_view.draw()
        self.surface.blit(self.battle_card_view.surface, (0,0))

    def update(self):
        pygame.display.update()

    def end(self):
        pygame.quit()
        print("Ending {0}".format(__class__))

    def tick(self):

        super().tick()


    def process_event(self, new_event: model.Event):

        super().process_event(new_event)

