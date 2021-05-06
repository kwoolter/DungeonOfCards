from . view import *
import card_dungeon.model as model
import pygame
from .graphics import *

class BattleCardView(View):
    def __init__(self, width : int, height : int):
        super().__init__(width=width, height=height)
        self.model = model
        self.surface = None
        self.fg = Colours.WHITE
        self.bg = Colours.DARK_GREEN

    def initialise(self, model : model.BattleCard):
        self.model = model
        self.surface = pygame.Surface((self.width, self.height))

    def draw(self):
        pane_rect = self.surface.get_rect()
        x,y = pane_rect.midtop
        size = 24
        self.surface.fill(self.bg)
        draw_text(self.surface, self.model.name, x,y + int(size/2),
                  size = size,
                  fg_colour=self.fg,
                  bg_colour=self.bg)

        size=16
        y+= 24
        dy = 16

        extras = ""
        if self.model.is_attack_unblockable is True:
            extras += "X"
            self.is_attack_unblockable = False
        if self.model.is_quick is True:
            extras += "!"
        if self.model.new_card_count != 0:
            extras += f" {self.model.new_card_count:+d} cards"

        if extras != "":
            draw_text(self.surface, extras, x, y + int(size / 2),
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            y+=dy


        for k,v in self.model.attacks.items():
            msg = f"Attack {k.name}:{v}"
            draw_text(self.surface, msg, x, y + int(size / 2),
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            y+=dy

        for k,v in self.model.blocks.items():
            msg = f"Block {k.name}:{v}"
            draw_text(self.surface, msg, x, y + int(size / 2),
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            y+=dy

        for k,v in self.model.heals.items():
            msg = f"Heal by {v} if {k.name}"
            draw_text(self.surface, msg, x, y + int(size / 2),
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            y+=dy

        for k,v in self.model.effects.items():
            msg = f"Effect {v.name} if {k.name}"
            draw_text(self.surface, msg, x, y + int(size / 2),
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            y+=dy


