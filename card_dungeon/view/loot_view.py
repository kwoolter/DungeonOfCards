from .view import *
from . card_views import LootCardView
from .graphics import *
import card_dungeon.model as model

class LootView(View):
    def __init__(self, name: str, width: int, height: int):
        super().__init__(name=name, width=width, height=height)
        self.model = None
        self.surface = None
        self.fg = Colours.DARK_GREEN
        self.bg = Colours.WHITE

        self.text_size = 20
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), self.text_size)

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

        self.surface.fill(self.bg)

        pane_rect = self.surface.get_rect()

        padding = 4
        x=padding
        y=0

        for i,card in enumerate(self.model.hand):

            cv = LootCardView(name=f"Loot Card {i}", width=self.card_width, height=self.card_height)
            view_rect = cv.rect
            view_rect.x = x
            view_rect.centery = pane_rect.centery

            cv.initialise(card)
            cv.draw()
            self.surface.blit(cv.surface, view_rect)

            # Register card view as a child and add a click zone
            self.add_child_view(cv, pos=view_rect.topleft)
            self.add_click_zone(f"Loot Card:{i+1}",view_rect )

            x+= view_rect.width + padding



