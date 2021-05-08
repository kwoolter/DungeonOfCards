from . view import *
import card_dungeon.model as model
import pygame
from .graphics import *

class CharacterView(View):
    def __init__(self, width : int, height : int):
        super().__init__(width=width, height=height)
        self.model = None
        self.surface = None
        self.is_highlighted = False
        self.bg = Colours.WHITE
        self.fg = Colours.DARK_GREEN

    def initialise(self, model : model.BaseCharacter):
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

        # Draw Character name and type
        pane_rect = self.surface.get_rect()
        x,y = pane_rect.midtop
        size = 24
        y += int(size / 2) + 4

        msg = f"{self.model.name} the {self.model.type.value}"
        draw_text(self.surface, msg, x,y,
                  size = size,
                  fg_colour=self.fg,
                  bg_colour=self.bg)

        # Is the character dead?
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
        y+=10
        padding = 4
        heart_img = View.IMAGE_MANAGER.get_skin_image(tile_name=model.CardFeature.HEAL)

        x = int(pane_rect.width - ((heart_img.get_rect().width + padding) * self.model.health))/2
        for i in range(self.model.health):
            self.surface.blit(heart_img, (x,y))
            x+=heart_img.get_rect().width + 4

        # Draw the current active effects
        y+=20
        x = pane_rect.centerx
        size = 18

        for k,v in self.model.effects.items():
            y += 16
            img = View.IMAGE_MANAGER.get_skin_image(tile_name=k)
            self.surface.blit(img, (x, y))
            msg = f" : {v}"
            draw_text(self.surface, msg, x, y,
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)

        # Draw the image of the character
        img = View.IMAGE_MANAGER.get_skin_image(tile_name=self.model.type)
        img_rect = img.get_rect()
        img_rect.centerx = pane_rect.centerx
        img_rect.bottom = pane_rect.bottom - 8
        self.surface.blit(img, img_rect)