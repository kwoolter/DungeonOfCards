import os
import pygame
import logging

class ImageManager():

    image_cache = {}
    skins = {}
    sprite_sheets = {}
    initialised = False

    DEFAULT_SKIN = "default"
    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    def __init__(self):
        pass

    def initialise(self):
        print("Initialising {0}".format(__class__))
        ImageManager.initialised = True

    def get_image(self, image_file_name: str, width: int = 0, height: int = 0):

        transparent = pygame.Color(0, 255, 0)

        if image_file_name not in ImageManager.image_cache.keys():

            if image_file_name in self.sprite_sheets.keys():
                file_name, rect = self.sprite_sheets[image_file_name]
                filename = ImageManager.RESOURCES_DIR + file_name
                logging.info("Loading image {0} from {1} at {2}...".format(image_file_name, filename, rect))

                image_sheet = spritesheet(filename)
                original_image = image_sheet.image_at(rect)
            else:
                filename = ImageManager.RESOURCES_DIR + image_file_name
                logging.info("Loading image {0}...".format(filename))
                image_sheet = spritesheet(filename)
                original_image = image_sheet.image_at()

            try:
                # Crop and blank space around the image
                smallest_size = original_image.get_bounding_rect()
                print(f'{image_file_name}:{original_image.get_rect()} smallest={smallest_size}')
                cropped_image = pygame.Surface((smallest_size.width, smallest_size.height))
                cropped_image.fill(transparent)
                cropped_image.blit(original_image, dest=(0,0), area= smallest_size)
                cropped_image.set_colorkey(transparent)

                # Scale the image if requested
                if width > 0 or height > 0:
                    cropped_image = pygame.transform.scale(cropped_image, (width, height))

                # Store the image in the cache
                r = cropped_image.get_rect()
                ImageManager.image_cache[image_file_name] = cropped_image

                logging.info(f"Image {filename} loaded and scaled to {r.width}x{r.height} and cached.")

            except Exception as err:
                print(str(err))

        return self.image_cache[image_file_name]

    def get_skin_image(self, tile_name: str, skin_name: str = DEFAULT_SKIN, tick=0, width: int = 0, height: int = 0):

        if skin_name not in ImageManager.skins.keys():
            raise Exception("Can't find specified skin {0}".format(skin_name))

        name, tile_map = ImageManager.skins[skin_name]

        if tile_name not in tile_map.keys():
            name, tile_map = ImageManager.skins[ImageManager.DEFAULT_SKIN]
            if tile_name not in tile_map.keys():
                raise Exception("Can't find tile name '{0}' in skin '{1}'!".format(tile_name, skin_name))

        tile_file_names = tile_map[tile_name]

        image = None

        if tile_file_names is None:
            image = None
        elif isinstance(tile_file_names, tuple):
            if tick == 0:
                tile_file_name = tile_file_names[0]
            else:
                tile_file_name = tile_file_names[tick % len(tile_file_names)]

            image = self.get_image(image_file_name=tile_file_name, width=width, height=height)

        else:
            image = self.get_image(tile_file_names, width=width, height=height)

        return image

class View():

    IMAGE_MANAGER = None

    def __init__(self, width: int = 0, height: int = 0):
        self._debug = False
        self.tick_count = 0

        self.height = height
        self.width = width

        self.surface = None

        # Dictionary of clickable areas in the view
        self.click_zones = {}

    def initialise(self):
        self.clear_click_zones()

    def clear_click_zones(self):
        self.click_zones = {}

    def add_click_zone(self, zone_name : str, zone_rect):
        self.click_zones[zone_name] = zone_rect

    # See if a click landed in a known zone in the view
    def is_zone_clicked(self, pos):
        zone = None
        for k,v in self.click_zones.items():
            if v.collidepoint(pos) == True:
                zone = k
                break
        return zone

    def tick(self):
        self.tick_count += 1

    def debug(self, debug_on: bool = None):

        if debug_on is None:
            self._debug = not self._debug
        else:
            self._debug = debug_on

    def draw(self):
        pass

    def process_event(self, args):
        print(f"{__class__}: Procssing event {args}")


    def end(self):
        print(f"Ending {__class__}")



class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
        except Exception as err:
            print('Unable to load spritesheet image:', filename)
            raise err

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle=None, colorkey=None):
        if rectangle is None:
            rectangle = self.sheet.get_rect()
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, depth=24)
        key = (0, 255, 0)
        image.fill(key)
        image.set_colorkey(key)
        image.blit(self.sheet, (0, 0), rect)

        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)