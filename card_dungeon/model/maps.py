import logging
from card_dungeon.model.doc_enums import *
import numpy as np


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
    def __init__(self, name:str):
        self.name = name
        self.current_room_id = 1
        self.rooms = {}
        self.tiles = None
        self.visible = set()

    def initialise(self):
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
    my_map.generate()

    current_room = my_map.get_room()
    current_room.print()

    current_room = my_map.move(Direction.NORTH)
    current_room.print()

    current_room = my_map.move(Direction.EAST)
    current_room.print()



if __name__ == "__main__":
    test()