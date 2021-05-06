import card_dungeon.model as model

class ImageManager():

    def __init__(self):
        pass

    @staticmethod
    def initialise():
        print("Initialising {0}".format(__class__))

class View():
    image_manager = ImageManager()
    ImageManager.initialise()

    def __init__(self, width: int = 0, height: int = 0):
        self._debug = False
        self.tick_count = 0
        self.height = height
        self.width = width
        self.surface = None

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