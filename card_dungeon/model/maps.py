import logging
import random

import numpy as np

from card_dungeon.model.doc_enums import *


class Room:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.links = {}

    def add_link(self, direction: Direction, to_room_id: int):
        self.links[direction] = to_room_id

    @property
    def link_key(self):
        key = ""
        for direction in Direction:
            if direction in self.links.keys():
                key += direction.value[0]
            else:
                key += "_"

        return key


    def print(self):
        print(f"Room: {self.name} ({self.link_key})")
        for k, v in self.links.items():
            print(f"\t{k.value} to room {v}")


class Map():

    DIRECTION_VECTORS = {Direction.NORTH: (0, -1),
                         Direction.SOUTH: (0, 1),
                         Direction.WEST: (-1, 0),
                         Direction.EAST: (1, 0)}

    def __init__(self, name:str):
        self.name = name
        self.current_room_id = 56
        self.max_width = 10
        self.max_height = 10
        self.max_rooms = 10
        self.rooms = {}
        self.tiles = None
        self.filled_tiles = None
        self.visible = set()

    def initialise(self):
        self.filled_tiles = {}
        self.visible = set()
        self.max_width = 10
        self.max_height = 10
        self.max_rooms = 10
        self.visible.add(self.current_room_id)

    def print(self):
        print(f"Map {self.name} with {len(self.rooms)} rooms")
        for room in self.rooms.values():
            room.print()

    def add_room(self, new_room: Room, is_visible = False):
        self.rooms[new_room.id] = new_room
        if is_visible:
            self.visible.add(new_room.id)

    def add_link(self, from_id:int, to_id:int, direction: Direction):

        assert from_id in self.rooms.keys(), f"add_link:Room {from_id} does not exist in map {self.name}"
        assert to_id in self.rooms.keys(), f"add_link:Room {from_id} does not exist in map {self.name}"
        assert direction in Direction, f"add_link: Direction {direction} is not a valid direction"

        from_room = self.rooms[from_id]
        from_room.add_link(direction, to_id)

        to_room = self.rooms[to_id]
        to_room.add_link(DIRECTION_REVERSE[direction],from_id)

    def get_room(self, room_id: int = None):
        if room_id is None:
            room_id = self.current_room_id
        return self.rooms.get(room_id, None)

    def is_visible(self, room_id:int = None):

        # If no room specified assume we are moving from the current room
        if room_id is None:
            room_id = self.current_room_id

        return room_id in self.visible

    def move(self, direction : Direction, from_id:int = None):

        # If no room specified assume we are moving from the current room
        if from_id is None:
            from_id = self.current_room_id

        assert from_id in self.rooms.keys(), f"move:Room {from_id} does not exist in map {self.name}"
        assert direction in Direction, f"move: Direction {direction} is not a valid direction"

        from_room = self.rooms.get(from_id, None)

        assert from_id != None, f"move:Room {from_id} does not exist in map {self.name}"

        to_room_id = from_room.links.get(direction, None)

        if to_room_id != None:
            new_room = self.rooms[to_room_id]
            self.current_room_id = to_room_id
            self.visible.add(self.current_room_id)
            logging.info(f"move:Moving {direction} from Room {from_id} to Room {new_room.id}")
        else:
            logging.info(f"move:Room {from_id}: no link {direction}")
            new_room = None

        return new_room

    def build_tile_map(self, room_id):
        self.tiles=np.array()
        used_tiles = []
        x=0
        y=0

    def navigate(self, room_id:int):
        pass


    def generate_random(self):
        new_room_id = 1
        self.filled_tiles = {}
        x = y = 0

        self.add_random_room(x,y,new_room_id)

    def add_random_room(self, x: int, y:int, new_room_id):

        logging.info(f"Attempting to add new room {new_room_id} at {x},{y}")

        if (x,y) in self.filled_tiles.keys():
            logging.info(f"Adding new room {new_room_id}: Tile {x},{y} is already occupied")
            return False

        if new_room_id > self.max_rooms:
            logging.info(f"Adding new room {new_room_id}: Reached maximum number of rooms {self.max_rooms}")
            return False

        if x<0 or x > self.max_width or y<0 or y > self.max_height:
            logging.info(f"Attempting to add new room {new_room_id} at {x},{y}: Hit the edge of the max")
            return False

        new_room = Room(new_room_id, f"Room {new_room_id}")
        self.add_room(new_room)
        self.filled_tiles[(x,y)] = new_room_id
        next_room_id = new_room_id + 1


        for d in Direction:
            if random.random() > 0.5:
                dx,dy = Map.DIRECTION_VECTORS[d]
                if self.add_random_room(x+dx,y+dy, next_room_id):
                    self.add_link(new_room_id,next_room_id, d)
                    next_room_id += 1

            if new_room_id > self.max_rooms:
                break

        return True

    def generate_random2(self):

        self.filled_tiles = {}
        links_added = 0
        rooms_linked = 0

        new_room_id = 1
        for x in range(self.max_width):
            for y in range(self.max_height):
                new_room = Room(new_room_id, f"{new_room_id}")
                self.add_room(new_room, is_visible=True)
                self.filled_tiles[(x,y)] = new_room
                new_room_id+=1

        start_x, start_y = (5,5)
        self.add_links(start_x, start_y)
        new_room =self.filled_tiles[(start_x,start_y)]


        while rooms_linked < 80:
            directions = list(new_room.links.keys())
            random.shuffle(directions)
            for d in directions:
                dx, dy = Map.DIRECTION_VECTORS[d]
                if self.add_links(start_x + dx, start_y + dy):
                    rooms_linked += 1
                start_x += dx
                start_y += dy



    def add_links(self, x: int, y:int):

        links_added = 0

        if x < 0 or x >= self.max_width or y < 0 or y >= self.max_height:
            return links_added == 0

        room = self.filled_tiles[(x, y)]
        room_id = room.id

        logging.info(f"Attempting to link up room {room_id} at {x},{y}")

        directions = list(
            set(Direction) -
            set(room.links.keys())
        )
        random.shuffle(directions)

        for d in directions:
            if random.random() > 0.7 or len(room.links) == 0:
                dx,dy = Map.DIRECTION_VECTORS[d]
                if x+dx < 0 or x+dx >= self.max_width or y+dy < 0 or y+dy >= self.max_height:
                    continue
                next_room_id = self.filled_tiles[(x+dx,y+dy)]
                self.add_link(room_id, next_room_id.id, d)
                links_added += 1

        return links_added > 0

    def generate(self):

        # Create a list of basic rooms
        rooms = [Room(i, f"Room {i}") for i in range(20)]
        for room in rooms:
            self.add_room(room)

        # Link up the rooms
        self.add_link(1, 2, Direction.NORTH)
        self.add_link(1, 3, Direction.EAST)
        self.add_link(1, 4, Direction.SOUTH)
        self.add_link(1, 5, Direction.WEST)
        self.add_link(2, 6, Direction.EAST)
        self.add_link(6, 10, Direction.EAST)
        self.add_link(3, 7, Direction.EAST)
        self.add_link(4, 8, Direction.SOUTH)
        self.add_link(7, 9, Direction.SOUTH)
        self.add_link(10,7, Direction.SOUTH)
        self.add_link(9,11, Direction.SOUTH)
        self.add_link(11,12, Direction.WEST)
        self.add_link(12, 8, Direction.WEST)
        self.add_link(3, 13, Direction.SOUTH)
        self.add_link(4, 13, Direction.EAST)
        self.add_link(9, 13, Direction.WEST)
        self.add_link(12, 13, Direction.NORTH)
        self.add_link(7,14, Direction.EAST)
        self.add_link(14,16, Direction.EAST)
        self.add_link(14,17, Direction.SOUTH)
        self.add_link(17,18, Direction.SOUTH)
        self.add_link(14,15, Direction.NORTH)


        # Set starting location
        self.current_room_id = 1


def test():

    logging.basicConfig(level=logging.INFO)

    my_map = Map("Test Map")
    my_map.initialise()
    my_map.generate_random2()
    my_map.print()

    current_room = my_map.get_room()
    current_room.print()




if __name__ == "__main__":
    test()