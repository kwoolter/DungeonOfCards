import card_dungeon.model as model
from .graphics import *
from .view import *


class CharacterView(View):
    def __init__(self, width: int, height: int):
        super().__init__(width=width, height=height)
        self.model = None
        self.surface = None
        self.is_highlighted = False
        self.bg = Colours.WHITE
        self.fg = Colours.DARK_GREEN

    def initialise(self, model: model.BaseCharacter):
        self.model = model
        self.surface = pygame.Surface((self.width, self.height))

    def draw(self):

        self.surface.fill(self.bg)

        margin = 8

        # Draw the border of the card
        pane_rect = self.surface.get_rect()
        border = pane_rect
        border.inflate_ip(-margin, -margin)
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
        x, y = pane_rect.midtop
        size = 24
        y += int(size / 2) + 4
        header_rect=pygame.Rect(border.x,border.y,border.width, size)
        pygame.draw.rect(self.surface,
                         fg,
                         header_rect)

        msg = f"{self.model.name} the {self.model.type.value}"
        draw_text(self.surface, msg, x, y,
                  size=size,
                  fg_colour=self.bg,
                  bg_colour=self.fg)

        # Draw the image of the character
        img = View.IMAGE_MANAGER.get_skin_image(tile_name=self.model.type)
        img_rect = img.get_rect()
        img_rect.centerx = pane_rect.centerx
        img_rect.bottom = pane_rect.bottom - 16
        self.surface.blit(img, img_rect)

        # Is the character dead?
        if self.model.is_dead is True:
            x, y = pane_rect.center
            size = 40
            msg = "*** DEAD ***"
            draw_text(self.surface,
                      msg,
                      x, y,
                      size=size,
                      fg_colour=self.bg,
                      bg_colour=self.fg)
            return

        # Draw current health
        y += 16
        padding = 4
        heart_img = View.IMAGE_MANAGER.get_skin_image(tile_name=model.CardFeature.HEAL)
        img_rect = heart_img.get_rect()

        x = int(pane_rect.width - ((img_rect.width + padding) * self.model.health)) / 2
        x=16
        for i in range(self.model.health):
            if i == 5:
                y+=img_rect.height + padding
                x = 16
            self.surface.blit(heart_img, (x, y))
            x += heart_img.get_rect().width + 4

        # Draw the current active effects
        y += img_rect.height + padding
        x = 10
        size = 18

        for k, v in self.model.effects.items():
            img = View.IMAGE_MANAGER.get_skin_image(tile_name=k)
            img_rect = img.get_rect()
            img_rect.topleft=(x,y)
            self.surface.blit(img, img_rect)
            msg = f" {v} "
            draw_text(self.surface,
                      msg,
                      img_rect.centerx,
                      img_rect.bottom,
                      size=size,
                      fg_colour=self.bg,
                      bg_colour=self.fg)

            x += img_rect.width + padding


