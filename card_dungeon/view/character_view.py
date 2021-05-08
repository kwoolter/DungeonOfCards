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

        # Draw Character name and type
        pane_rect = self.surface.get_rect()
        x,y = pane_rect.midtop
        size = 24
        self.surface.fill(self.bg)
        msg = f"{self.model.name} the {self.model.type}"
        draw_text(self.surface, msg, x,y + int(size/2),
                  size = size,
                  fg_colour=self.fg,
                  bg_colour=self.bg)

        # Is the character dead
        if self.model.is_dead is True:
            x,y = pane_rect.center
            size = 40
            msg = "*** DEAD ***"
            draw_text(self.surface,
                      msg,
                      x, y,
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            return

        # Draw current health
        y+=32
        size = 18
        msg = f"Health : {self.model.health}"
        draw_text(self.surface, msg, x,y,
                  size = size,
                  fg_colour=self.fg,
                  bg_colour=self.bg)


        # Draw the current active effects
        for k,v in self.model.effects.items():
            y += 16
            msg = f"{k.name} : {v}"
            draw_text(self.surface, msg, x, y,
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
