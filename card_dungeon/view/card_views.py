from . view import *
import card_dungeon.model as model
import pygame
from .graphics import *

class BattleCardView(View):
    def __init__(self, width : int, height : int):
        super().__init__(width=width, height=height)
        self.model = model
        self.surface = None
        self.fg = Colours.DARK_GREEN
        self.bg = Colours.LIGHT_GREY
        self.is_highlighted = False
        self.is_concealed = False

    def initialise(self, model : model.BattleCard):
        self.model = model
        self.surface = pygame.Surface((self.width, self.height))

    def draw(self):

        self.surface.fill(self.bg)

        # Draw the border of the card
        pane_rect = self.surface.get_rect()
        border = pane_rect
        border.inflate_ip(-8,-8)
        if self.is_highlighted is True:
            fg = Colours.YELLOW
            border_width = 5
        else:
            fg = self.fg
            border_width = 3

        pygame.draw.rect(self.surface,
                         fg,
                         border,
                         border_width)

        # Draw the name of the card
        x,y = pane_rect.midtop
        size = 24

        draw_text(self.surface, self.model.name, x,y + int(size/2),
                  size = size,
                  fg_colour=self.fg,
                  bg_colour=self.bg)

        # If the card is concealed then we don't need to show any more details
        if self.is_concealed is True:
            x,y = pane_rect.center
            draw_text(self.surface,
                      "?",
                      x, y,
                      size=60,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            return

        # Draw any extra properties of the card
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

        # Draw the card attacks
        for k,v in self.model.attacks.items():
            msg = f"Attack {k.name}:{v}"
            draw_text(self.surface, msg, x, y + int(size / 2),
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            y+=dy

        # Draw the card blocks
        for k,v in self.model.blocks.items():
            msg = f"Block {k.name}:{v}"
            draw_text(self.surface, msg, x, y + int(size / 2),
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            y+=dy

        # Draw the card heals
        for k,v in self.model.heals.items():
            msg = f"Heal by {v} if {k.name}"
            draw_text(self.surface, msg, x, y + int(size / 2),
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            y+=dy

        # Draw the card effects
        for k,v in self.model.effects.items():
            msg = f"Effect {v.name} if {k.name}"
            draw_text(self.surface, msg, x, y + int(size / 2),
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            y+=dy


