from . view import *
import card_dungeon.model as model
import pygame
from .graphics import *

class CharacterView(View):
    def __init__(self, width : int, height : int):
        super().__init__(width=width, height=height)
        self.model = model
        self.surface = None
        self.fg = Colours.WHITE
        self.bg = Colours.DARK_GREEN

    def initialise(self, model : model.BaseCharacter):
        self.model = model
        self.surface = pygame.Surface((self.width, self.height))

    def draw(self):
        pane_rect = self.surface.get_rect()
        x,y = pane_rect.midtop
        size = 24
        self.surface.fill(self.bg)
        msg = f"{self.model.name} the {self.model.type}"
        draw_text(self.surface, msg, x,y + int(size/2),
                  size = size,
                  fg_colour=self.fg,
                  bg_colour=self.bg)