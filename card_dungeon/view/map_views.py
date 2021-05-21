from .view import *
from .graphics import *
import card_dungeon.model as model
from card_dungeon.model.doc_enums import *

class MapView(View):

    DIRECTION_VECTORS = {Direction.NORTH:(0,-1),
                         Direction.SOUTH:(0,1),
                         Direction.WEST:(-1,0),
                         Direction.EAST:(1,0)}

    ZOOM_SIZES = [32, 48, 64, 96, 128 ]

    def __init__(self, name:str, width:int, height:int):
        super().__init__(name=name, width=width,height=height)

        self.model = None
        self.fg = Colours.GREY
        self.bg = Colours.WHITE
        self.bg_highlight = Colours.YELLOW
        self.zoom_factor = 1
        self.room_width = MapView.ZOOM_SIZES[self.zoom_factor]
        self.room_height = MapView.ZOOM_SIZES[self.zoom_factor]

        self.drawn = []

    def initialise(self, model: model.Map):
        self.model = model
        self.surface = pygame.Surface((self.width, self.height))
        self.drawn=[]

    def zoom(self, dz: int = 1):
        self.zoom_factor = max(min(self.zoom_factor + dz, len(MapView.ZOOM_SIZES)-1),0)

    def draw(self):

        # Reset the list to track which rooms we have drawn so far
        self.drawn=[]

        pane_rect = self.surface.get_rect()

        # Fill the view with graph paper-like grid of squares
        self.surface.fill(Colours.WHITE)
        grid_size = MapView.ZOOM_SIZES[self.zoom_factor]
        grid_colour = (190, 244, 255)

        for x in range(pane_rect.x, pane_rect.width, grid_size):
            pygame.draw.line(self.surface, grid_colour, (x, pane_rect.top), (x, pane_rect.bottom), 2)

        for y in range(pane_rect.top, pane_rect.bottom, grid_size):
            pygame.draw.line(self.surface, grid_colour, (pane_rect.left, y), (pane_rect.right, y), 2)

        # Draw the map starting with the current room
        self.draw_room(self.model.current_room_id, pane_rect.centerx, pane_rect.centery)

        # Draw header
        size = 40
        draw_text(self.surface,
                  f"Map of {self.model.name}",
                  pane_rect.centerx,
                  pane_rect.top + int(size/2),
                  size=size,
                  fg_colour=self.fg,
                  bg_colour=None)

        # Draw a border
        pygame.draw.rect(self.surface,
                         self.fg,
                         pane_rect,
                         8)

    def draw_room(self, room_id:int, x:int, y:int):

        # If we have already drawn this room then exit
        if room_id in self.drawn:
            return

        # Get the room object using the room ID
        room = self.model.get_room(room_id)

        # Get what the room should look like
        img = View.IMAGE_MANAGER.get_skin_image(tile_name=room.link_key)

        # Scale image based on ZOOM factor
        room_width = MapView.ZOOM_SIZES[self.zoom_factor]
        room_height = MapView.ZOOM_SIZES[self.zoom_factor]
        img = pygame.transform.scale(img, (room_width, room_height))

        # Draw the room at the specified coordinates
        img_rect = img.get_rect()
        img_rect.center = (x,y)

        fg = self.fg
        bg = self.bg
        if room_id == self.model.current_room_id:
            bg,fg = fg,bg
            pygame.draw.rect(self.surface,
                             self.bg_highlight,
                             img_rect)

        self.surface.blit(img, img_rect)

        draw_text(self.surface,
                  f" {room_id} ",
                  img_rect.centerx,
                  img_rect.centery,
                  size=18,
                  fg_colour=fg,
                  bg_colour=bg)

        # Register that we have drawn this room now
        self.drawn.append(room_id)

        # Recursively draw all of the rooms linked to this room in the map
        for direction, room_id in room.links.items():

            if self.model.is_visible(room_id) is False:
                continue

            # get the vector to change the x,y coordinated by based on direction
            dx,dy = MapView.DIRECTION_VECTORS[direction]

            # Draw the linked room
            self.draw_room(room_id, x + dx*room_width, y+dy*room_height)


