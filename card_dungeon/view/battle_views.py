from .view import *
from .graphics import *
import card_dungeon.model as model
from .card_views import BattleCardView


class BattleRoundView(View):

    def __init__(self, width: int, height: int):
        super().__init__(width=width, height=height)
        self.model = None
        self.surface = None
        self.fg = Colours.DARK_GREEN
        self.bg = Colours.WHITE

        self.player_card_view = None
        self.enemy_card_view = None

        self.card_width = 150
        self.card_height = 180

    def initialise(self, model: model.Battle):
        self.model = model
        self.surface = pygame.Surface((self.width, self.height))

        self.player_card_view = BattleCardView(width=self.card_width, height=self.card_height)
        self.player_card_view.initialise(self.model.player_selected_card)
        self.enemy_card_view = BattleCardView(width=self.card_width, height=self.card_height)
        self.enemy_card_view.initialise(self.model.enemy_cards.hand[0])

    def draw(self):
        self.surface.fill(self.bg)

        pane_rect = self.surface.get_rect()
        padding = 10

        # Draw the border of the card
        border = pane_rect
        border.inflate_ip(-8, -8)
        fg = self.fg
        border_width = 3

        pygame.draw.rect(self.surface,
                         fg,
                         border,
                         border_width)

        if self.model is None:
            return


        # Draw the batle contestants
        x, y = pane_rect.midtop
        size = 24
        msg = f"{self.model.player.name} vs. {self.model.enemy.name} Round {self.model.round}"

        draw_text(self.surface,
                  msg,
                  x,
                  y + int(size / 2),
                  size=size,
                  fg_colour=self.fg,
                  bg_colour=self.bg)

        self.player_card_view.initialise(self.model.player_selected_card)
        # self.enemy_card_view.initialise(self.model.enemy_round_card)

        self.player_card_view.draw()
        card_rect = self.player_card_view.surface.get_rect()
        card_rect.x = pane_rect.x + padding
        card_rect.centery = pane_rect.centery
        self.surface.blit(self.player_card_view.surface, card_rect)

        self.enemy_card_view.draw()
        card_rect = self.enemy_card_view.surface.get_rect()
        card_rect.right = pane_rect.right - padding
        card_rect.centery = pane_rect.centery
        self.surface.blit(self.enemy_card_view.surface, card_rect)
