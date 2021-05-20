from .view import *
from . card_views import LootCardView
from .graphics import *
import card_dungeon.model as model

class LootView(View):
    def __init__(self, name: str, width: int, height: int):
        super().__init__(name=name, width=width, height=height)

        self.model = None
        self.surface = None
        self.fg = Colours.DARK_GREY
        self.bg = Colours.LIGHT_GREY

        self.text_size = 20
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), self.text_size)

        self.button_width = 200
        self.button_text_size = 48
        self.button_height = self.button_text_size + 4
        self.button_font = pygame.font.SysFont(pygame.font.get_default_font(), self.button_text_size)

        self.card_width = 150
        self.card_height = 180

        # Default this view is not visible
        self.is_visible = False

    def initialise(self, model:model.CardManager):
        self.model = model
        self.surface = pygame.Surface((self.width, self.height))

    def draw(self):

        if self.is_visible is False:
            return

        pane_rect = self.surface.get_rect()

        # fill and draw a border
        self.surface.fill(self.bg)

        pygame.draw.rect(self.surface,
                         self.fg,
                         pane_rect,
                         8)

        padding = 4
        x=padding*2
        y=padding*2

        # Draw each of the loot cards
        for i,card in enumerate(self.model.hand):

            cv = LootCardView(name=f"Loot Card {i}", width=self.card_width, height=self.card_height)
            view_rect = cv.rect
            view_rect.x = x
            view_rect.y = y

            cv.initialise(card)
            cv.is_highlighted = card == self.model.selected_card
            cv.draw()
            self.surface.blit(cv.surface, view_rect)

            # Register card view as a child and add a click zone
            self.add_child_view(cv, pos=view_rect.topleft)
            self.add_click_zone(f"Loot Card:{i+1}",view_rect )

            # Change colours if this is THE selected card
            fg = Colours.WHITE
            if cv.is_highlighted:
                bg = Colours.GOLD
            else:
                bg = Colours.GREY

            draw_text(self.surface,
                      f" {i + 1} ",
                      x + int(cv.width / 2),
                      y + cv.height,
                      64,
                      fg_colour=fg,
                      bg_colour=bg)

            x += cv.width + padding


        # Draw the 'Choose' button
        fg = Colours.WHITE
        bg = Colours.GREEN
        border_fg = Colours.DARK_GREEN
        button_rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        button_rect.centerx = pane_rect.centerx
        button_rect.bottom = pane_rect.bottom - padding * 2

        self.add_click_zone("Choose Button", button_rect)

        # Draw the button
        pygame.draw.rect(self.surface,
                         bg,
                         button_rect)

        # Draw the border
        pygame.draw.rect(self.surface,
                         border_fg,
                         button_rect,
                         4)

        # Draw the button text
        text_size = self.button_text_size
        text_rect = pygame.Rect(0, 0, self.button_width - 10, text_size)
        text_rect.center = button_rect.center

        msg = f"Choose"

        # msg = drawText(self.surface,
        #                msg,
        #                color=fg,
        #                rect=text_rect,
        #                font=self.button_font,
        #                bkg=bg
        #                )

        draw_text(surface=self.surface,
                  msg=msg,
                  x=button_rect.centerx,
                  y=button_rect.centery,
                  size=self.button_text_size,
                  fg_colour=fg,
                  bg_colour=bg)

        # pygame.draw.rect(self.surface,
        #                  Colours.BLACK,
        #                  text_rect,
        #                  1)


