import card_dungeon.model as model
from .graphics import *
from .view import *


class BattleCardView(View):
    def __init__(self, width: int, height: int):
        super().__init__(width=width, height=height)
        self.model = model
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

        # Draw the name of the card
        x, y = pane_rect.midtop
        size = 24

        draw_text(self.surface, self.model.name, x, y + int(size / 2),
                  size=size,
                  fg_colour=self.fg,
                  bg_colour=self.bg)

        # If the card is concealed then we don't need to show any more details
        if self.is_concealed is True:
            x, y = pane_rect.center
            draw_text(self.surface,
                      "?",
                      x, y,
                      size=60,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            return

        y += 20
        padding = 4

        # Draw the card attacks
        if len(self.model.attacks) > 0:
            for k, v in self.model.attacks.items():
                x = 10
                img = View.IMAGE_MANAGER.get_skin_image(tile_name=k)
                img_rect = img.get_rect()
                for i in range(v):
                    self.surface.blit(img, (x, y))
                    x += img_rect.width + padding
                y += img_rect.height + padding

        # Draw the card blocks
        if len(self.model.blocks) > 0:
            for k, v in self.model.blocks.items():
                x = 16
                img = View.IMAGE_MANAGER.get_skin_image(tile_name=k)
                img_rect = img.get_rect()
                for i in range(v):
                    self.surface.blit(img, (x, y))
                    x += img_rect.width + padding
                y += img_rect.height + padding

        # Draw the card heals
        if len(self.model.heals) > 0:

            size = 16

            # Get the heal image
            img = View.IMAGE_MANAGER.get_skin_image(tile_name=model.CardFeature.HEAL)
            img_rect = img.get_rect()

            # For each type of heal
            for k, v in self.model.heals.items():
                x = 16

                # Draw the number of hearts that you will heal by
                for i in range(v):
                    self.surface.blit(img, (x, y))
                    x += img_rect.width + padding

                # .. and what conditions need to be met
                msg = f"...if {k.name}"
                draw_text(self.surface, msg,
                          x,
                          y + img_rect.centery,
                          size=size,
                          fg_colour=self.fg,
                          bg_colour=self.bg,
                          centre=False)

                y += img_rect.height + padding

        # Draw the card effects
        if len(self.model.effects) > 0:

            x = 16
            size = 16

            # For each type of effect
            for k, v in self.model.effects.items():
                # Get the effect image
                img = View.IMAGE_MANAGER.get_skin_image(tile_name=v)
                img_rect = img.get_rect()
                img_rect.topleft = (x, y)
                self.surface.blit(img, (x, y))

                # If their is a condition on the effect other than ALL...
                if k != model.Outcome.ALL:

                    # Draw what outcome is required for effect to apply
                    msg = f"if {k.name}"
                    draw_text(self.surface, msg,
                              img_rect.centerx,
                              img_rect.bottom + 10,
                              size=size,
                              fg_colour=self.fg,
                              bg_colour=self.bg)

                x += img_rect.width + padding

            y += img_rect.height + padding

        # Draw any extra properties of the card
        x = 16

        if self.model.is_attack_unblockable is True:
            property_img = View.IMAGE_MANAGER.get_skin_image(tile_name=model.CardFeature.UNBLOCKABLE)
            self.surface.blit(property_img, (x, y))
            x += property_img.get_rect().width + padding

        if self.model.is_quick is True:
            property_img = View.IMAGE_MANAGER.get_skin_image(tile_name=model.CardFeature.QUICK)
            self.surface.blit(property_img, (x, y))
            x += property_img.get_rect().width + padding

        if self.model.new_card_count != 0:
            property_img = View.IMAGE_MANAGER.get_skin_image(tile_name=model.CardFeature.DEAL)
            self.surface.blit(property_img, (x, y))
            x += property_img.get_rect().width + padding
