from .view import *
from .graphics import *
import card_dungeon.model as model
from card_dungeon.model.doc_enums import *

class MapView(View):

    DIRECTION_VECTORS = {Direction.NORTH:(0,-1),
                         Direction.SOUTH:(0,1),
                         Direction.WEST:(-1,0),
                         Direction.EAST:(1,0)}

    def __init__(self, name:str, width:int, height:int):
        super().__init__(name=name, width=width,height=height)

        self.model = None
        self.fg = Colours.GREY
        self.bg = Colours.LIGHT_GREY
        self.bg_highlight = Colours.YELLOW
        self.room_width = 48
        self.room_height = 48

        self.drawn = []

    def initialise(self, model: model.Map):
        self.model = model
        self.surface = pygame.Surface((self.width, self.height))
        self.drawn=[]

    def draw(self):

        # Reset the list to track which rooms we have drawn so far
        self.drawn=[]

        # Fill and draw border
        self.surface.fill(self.bg)
        pane_rect = self.surface.get_rect()

        pygame.draw.rect(self.surface,
                         self.fg,
                         pane_rect,
                         8)


        # Draw the map starting with the current room
        self.draw_room(self.model.current_room_id, pane_rect.centerx, pane_rect.centery)


    def draw_room(self, room_id:int, x:int, y:int):

        # If we have already drawn this room then exit
        if room_id in self.drawn:
            return


        # Get the room object using the room ID
        room = self.model.get_room(room_id)

        # Get what the room should look like
        img = View.IMAGE_MANAGER.get_skin_image(tile_name=room.link_key,width=self.room_width, height=self.room_height)

        # Draw the room at the specified coordinates
        img_rect = img.get_rect()
        img_rect.topleft = (x,y)

        if room_id == self.model.current_room_id:
            pygame.draw.rect(self.surface,
                             self.bg_highlight,
                             img_rect)

        self.surface.blit(img, img_rect)

        # Register that we have drawn this room now
        self.drawn.append(room_id)

        # Recursively draw all of the rooms linked to this room in the map
        for direction, room_id in room.links.items():

            if self.model.is_visible(room_id) is False:
                continue

            # get the vector to change the x,y coordinated by based on direction
            dx,dy = MapView.DIRECTION_VECTORS[direction]

            # Draw the linked room
            self.draw_room(room_id, x + dx*self.room_width, y+dy*self.room_height)


