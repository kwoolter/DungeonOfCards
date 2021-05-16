import logging
import os

import pygame


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

    def get_image(self, image_file_name: str, width: int = 0, height: int = 0, crop=False):

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
                if crop is True:
                    smallest_size = original_image.get_bounding_rect()
                    print(f'{image_file_name}:{original_image.get_rect()} smallest={smallest_size}')
                    cropped_image = pygame.Surface((smallest_size.width, smallest_size.height))
                    cropped_image.fill(transparent)
                    cropped_image.blit(original_image, dest=(0, 0), area=smallest_size)
                    cropped_image.set_colorkey(transparent)

                    # Scale the image if requested
                    if width > 0 or height > 0:
                        cropped_image = pygame.transform.scale(cropped_image, (width, height))
                else:
                    cropped_image= original_image

                # Store the image in the cache
                r = cropped_image.get_rect()
                ImageManager.image_cache[image_file_name] = cropped_image

                logging.info(f"Image {filename} loaded and scaled to {r.width}x{r.height} and cached.")

            except Exception as err:
                print(str(err))

        return self.image_cache[image_file_name]

    def get_skin_image(self, tile_name: str, skin_name: str = DEFAULT_SKIN, tick=0, width: int = 0, height: int = 0, crop=False):

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

            image = self.get_image(image_file_name=tile_file_name, width=width, height=height, crop=crop)

        else:
            image = self.get_image(tile_file_names, width=width, height=height, crop=crop)

        return image


class View():
    IMAGE_MANAGER = None

    def __init__(self, name: str = None, width: int = 0, height: int = 0):

        # Properties
        self._debug = False
        self.tick_count = 0
        self.height = height
        self.width = width
        self.is_visible = True

        # If no view name specific then generate one
        if name is None:
            name = f"View:{id(self)}"

        self.name = name

        self.surface = None

        # Dictionary of clickable areas in the view
        self.click_zones = {}

        # Dictionary of child views Key=View Name, Value = (View, pos)
        self.child_views = {}

    @property
    def rect(self):
        if self.surface is not None:
            return self.surface.get_rect()
        else:
            return pygame.Rect(0, 0, self.width, self.height)

    def initialise(self):
        self.clear_child_views()
        self.clear_click_zones()

    def on_click(self, pos):
        """
        This method is called when a user clicks on a position that is within this view
        :param pos: where the used click inside this view
        :return: zone if we found a clickable zone either in this view or in a child view
        """
        zone = None

        # If this view is not visible then do not proceed
        if self.is_visible is False:
            return zone

        # Loop through the clickable zones in this view..
        for k, v in self.click_zones.items():

            # See if the specified position is within this zone
            # If it is then stop looking for a match
            if v.collidepoint(pos) == True:
                zone = k
                break

        # Override this method if you want to react to a user clicking on a zone in this view
        self.on_click_zone(zone)

        # If we didn't find a matching zone in this view then try all of the child views...
        if zone is None:
            for k, (v, vpos) in self.child_views.items():

                # Did we click somewhere on the child window?
                view_rect = v.rect
                view_rect.topleft = vpos

                # If child window contains the click point...
                if view_rect.collidepoint(pos):

                    # Adjust the specified pos to be relative to child window top left
                    vpos_x, vpos_y = vpos
                    pos_x, pos_y = pos
                    adj_pos = (pos_x - vpos_x, pos_y - vpos_y)

                    # Call on-click method for child window with an adjusted click position
                    zone = v.on_click(adj_pos)
                    if zone != None:
                        break

        return zone

    def on_click_zone(self, zone_name:str):
        if zone_name is None:
            print(f"Default on_click_zone(): View '{self.name}' general click")
        else:
            print(f"Default on_click_zone(): '{self.name}' Zone '{zone_name}' click")

    # Add a view that is a child of this view
    def add_child_view(self, new_view, name: str = None, pos=(0, 0)) -> str:
        if name is None:
            name = new_view.name
        self.child_views[name] = (new_view, pos)

        # logging.info(f"Added Child View {name} at {pos}")

        return name

    # Clear all child views from this view
    def clear_child_views(self):
        self.child_views = {}

    # Remove all clickable zones
    def clear_click_zones(self):
        self.click_zones = {}

    # Add a clickable zone to the view
    def add_click_zone(self, zone_name: str, zone_rect):
        self.click_zones[zone_name] = zone_rect

    def tick(self):
        self.tick_count += 1

    def debug(self, debug_on: bool = None):

        if debug_on is None:
            self._debug = not self._debug
        else:
            self._debug = debug_on

    def print(self):
        print(f"View {self.name} (tick:{self.tick_count}")

        print("Click Zones:")
        for k, v in self.click_zones.items():
            print(f"{k}:{v}")

        print("Child Views:")
        for k, v in self.child_views.items():
            print(f"{k}:{v}")

    def draw(self):
        pass

    def process_event(self, args):
        print(f"{__class__}: Processing event {args}")

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
