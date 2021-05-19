import card_dungeon.model as model
from .graphics import *
from .view import *


class BattleCardView(View):
    def __init__(self, name: str, width: int, height: int):
        super().__init__(name=name, width=width, height=height)
        self.model = None
        self.surface = None
        self.fg = Colours.DARK_GREEN
        self.bg = Colours.WHITE
        self.is_highlighted = False
        self.is_concealed = False

    def initialise(self, model: model.BattleCard):
        self.model = model
        self.surface = pygame.Surface((self.width, self.height))

    def draw(self):

        self.surface.fill(self.bg)

        # Draw the border of the card
        pane_rect = self.surface.get_rect()
        border = pane_rect
        border.inflate_ip(-8, -8)
        if self.is_highlighted is True:
            fg = Colours.GOLD
            border_width = 5
        else:
            fg = self.fg
            border_width = 3

        pygame.draw.rect(self.surface,
                         fg,
                         border,
                         border_width)

        if self.model is None:
            return

        # Draw the name of the card
        x, y = pane_rect.midtop
        size = 24
        header = pygame.Rect(border.x, border.y, border.width, size)
        pygame.draw.rect(self.surface,
                         self.fg,
                         header)

        if self.is_concealed is True:
            header_text = "????"
        else:
            header_text = self.model.name

        draw_text(self.surface,
                  header_text,
                  x, y + int(size / 2),
                  size=size,
                  fg_colour=self.bg,
                  bg_colour=self.fg)

        # If the card is concealed then we don't need to show any more details
        if self.is_concealed is True:
            x, y = pane_rect.center
            draw_text(self.surface,
                      " ? ",
                      x, y,
                      size=60,
                      fg_colour=self.bg,
                      bg_colour=self.fg)
            return

        padding = 4
        y += 24 + padding
        margin = 16

        # Draw the card attacks
        if len(self.model.attacks) > 0:
            for k, v in self.model.attacks.items():
                if v == 0:
                    continue
                x = margin
                img = View.IMAGE_MANAGER.get_skin_image(tile_name=k)
                img_rect = img.get_rect()
                for i in range(v):
                    self.surface.blit(img, (x, y))
                    x += img_rect.width + padding
                y += img_rect.height + padding

        # Draw the card blocks
        if len(self.model.blocks) > 0:
            for k, v in self.model.blocks.items():
                if v == 0:
                    continue
                x = margin
                img = View.IMAGE_MANAGER.get_skin_image(tile_name=k)
                img_rect = img.get_rect()
                for i in range(v):
                    self.surface.blit(img, (x, y))
                    x += img_rect.width + padding
                y += img_rect.height + padding

        # Draw the card heals
        if len(self.model.heals) != 0:

            size = 16

            # Get the heal/drain image
            heart_img = View.IMAGE_MANAGER.get_skin_image(tile_name=model.CardFeature.HEAL)
            drain_img = View.IMAGE_MANAGER.get_skin_image(tile_name=model.CardFeature.DRAIN)

            # For each type of heal
            for k, v in self.model.heals.items():
                x = margin

                # Pick the heart or drain image
                if v > 0:
                    img = heart_img
                else:
                    img = drain_img

                img_rect = img.get_rect()
                img_rect.topleft = (x,y)

                # Draw the number of hearts/drains that you will heal by
                for i in range(abs(v)):
                    self.surface.blit(img, img_rect)
                    x += img_rect.width + padding

                # If there is a condition on the effect other than ALL...
                if k != model.Outcome.ALL:
                    msg = f"{k.value}"
                    draw_text(self.surface, msg,
                              img_rect.centerx,
                              img_rect.bottom + int(size / 2) - 2,
                              size=size,
                              fg_colour=self.fg,
                              bg_colour=self.bg,
                              centre=True)

                y += img_rect.height + padding

        # Draw the card effects
        if len(self.model.effects) > 0:

            x = margin
            size = 16

            # For each type of effect
            for k, v in self.model.effects.items():
                # Get the effect image
                img = View.IMAGE_MANAGER.get_skin_image(tile_name=v)
                img_rect = img.get_rect()
                img_rect.topleft = (x, y)
                self.surface.blit(img, (x, y))

                # If there is a condition on the effect other than ALL...
                if k != model.Outcome.ALL:
                    # Draw what outcome is required for effect to apply
                    msg = f"{k.value}"
                    draw_text(self.surface, msg,
                              img_rect.centerx,
                              img_rect.bottom + int(size / 2) - 2,
                              size=size,
                              fg_colour=self.fg,
                              bg_colour=self.bg)

                x += img_rect.width + padding

            y += img_rect.height + padding + size

        # Draw any extra properties of the card
        x = margin

        if self.model.is_attack_unblockable:
            property_img = View.IMAGE_MANAGER.get_skin_image(tile_name=model.CardFeature.UNBLOCKABLE)
            self.surface.blit(property_img, (x, y))
            x += property_img.get_rect().width + padding

        if self.model.is_quick:
            property_img = View.IMAGE_MANAGER.get_skin_image(tile_name=model.CardFeature.QUICK)
            self.surface.blit(property_img, (x, y))
            x += property_img.get_rect().width + padding

        if self.model.new_card_count != 0:
            property_img = View.IMAGE_MANAGER.get_skin_image(tile_name=model.CardFeature.DEAL)
            self.surface.blit(property_img, (x, y))
            x += property_img.get_rect().width + padding


class LootCardView(View):
    def __init__(self, name: str, width: int, height: int):
        super().__init__(name=name, width=width, height=height)
        self.model = None
        self.surface = None
        self.fg = Colours.GOLD
        self.bg = Colours.WHITE
        self.is_highlighted = False

    def initialise(self, model: model.LootCard):
        self.model = model
        self.surface = pygame.Surface((self.width, self.height))

    def draw(self):

        self.surface.fill(self.bg)

        # Draw the border of the card
        pane_rect = self.surface.get_rect()
        border = pane_rect
        border.inflate_ip(-8, -8)
        if self.is_highlighted is True:
            fg = Colours.GOLD
            border_width = 5
        else:
            fg = self.fg
            border_width = 3

        pygame.draw.rect(self.surface,
                         fg,
                         border,
                         border_width)

        if self.model is None:
            return

        # Draw the name of the card
        x, y = pane_rect.midtop
        size = 24
        header = pygame.Rect(border.x, border.y, border.width, size)
        pygame.draw.rect(self.surface,
                         self.fg,
                         header)

        draw_text(self.surface, self.model.name, x, y + int(size / 2),
                  size=size,
                  fg_colour=self.bg,
                  bg_colour=self.fg)
