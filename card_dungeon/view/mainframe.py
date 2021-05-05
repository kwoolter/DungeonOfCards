import pygame
import os
import card_dungeon.model as model
from .graphics import Colours

class ImageManager():

    def __init__(self):
        pass

    def initialise(self):
        pass

class View():
    image_manager = ImageManager()

    def __init__(self, width: int = 0, height: int = 0):
        self._debug = False
        self.tick_count = 0
        self.height = height
        self.width = width
        self.surface = None

        View.image_manager.initialise()

    def initialise(self):
        pass

    def tick(self):
        self.tick_count += 1

    def debug(self, debug_on: bool = None):

        if debug_on is None:
            self._debug = not self._debug
        else:
            self._debug = debug_on

    def process_event(self, new_event: model.Event):
        print("Default View Class event process:{0}".format(new_event))


    def draw(self):
        pass

    def end(self):
        print("Ending {0}".format(__class__))


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


    def print(self):

        print("Printing Dark Work view...")



    def draw(self):

        pane_rect = self.surface.get_rect()

        x = 0
        y = 0

        self.surface.fill(Colours.RED)

    def update(self):
        pygame.display.update()

    def end(self):
        pygame.quit()
        print("Ending {0}".format(__class__))

    def tick(self):

        super().tick()


    def process_event(self, new_event: model.Event):

        super().process_event(new_event)

