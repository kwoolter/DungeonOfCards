from .view import *
from .graphics import *
import card_dungeon.model as model
from .card_views import BattleCardView
import time


class BattleRoundView(View):

    def __init__(self, width: int, height: int):
        super().__init__(width=width, height=height)
        self.model = None
        self.surface = None
        self.fg = Colours.DARK_GREEN
        self.bg = Colours.WHITE
        self.text_size = 20
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), self.text_size)

        self.player_card_view = None
        self.enemy_card_view = None

        self.card_width = 150
        self.card_height = 180

    def initialise(self, model: model.Battle):
        self.model = model
        self.surface = pygame.Surface((self.width, self.height))

        self.player_card_view = BattleCardView(width=self.card_width, height=self.card_height)
        self.player_card_view.initialise(self.model.player_selected_card)
        self.player_card_view.fg = Colours.BLUE

        self.enemy_card_view = BattleCardView(width=self.card_width, height=self.card_height)
        self.enemy_card_view.initialise(self.model.enemy_cards.default_hand_card )
        self.enemy_card_view.fg = Colours.RED

    def draw(self):
        self.surface.fill(self.bg)

        pane_rect = self.surface.get_rect()
        padding = 4

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


        # Draw the battle contestants
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

        # Draw the card that each contestant is going to play in this round
        self.player_card_view.initialise(self.model.player_selected_card)
        self.enemy_card_view.initialise(self.model.enemy_selected_card)

        self.player_card_view.is_concealed = self.model.player.is_confused
        self.enemy_card_view.is_concealed = self.model.player.is_blind

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

        # Draw the battle events
        size = self.text_size
        padding = 4

        # Create a rect that will contain each event line of text
        msg_rect = pygame.Rect(0,0,280,size)
        msg_rect.centerx = border.centerx
        msg_rect.y += size + padding

        # Loop through each recorded event...
        for event in self.model.events.events:

            # Pick the colour scheme for the event
            if event.name == model.Event.PLAYER_INFO:
                fg=Colours.BLUE
                bg=Colours.WHITE
            elif event.name == model.Event.ENEMY_INFO:
                fg=Colours.RED
                bg=Colours.WHITE
            else:
                fg=Colours.DARK_GREEN
                bg=self.bg

            msg_rect.y += padding


            msg = f"{event.description}"

            # Print each event description in chunks until we run out of msg to display
            while len(msg) > 0:
                pygame.draw.rect(self.surface,
                                 bg,
                                 msg_rect)

                msg = drawText(self.surface,
                         msg,
                         color = fg,
                         rect = msg_rect,
                         font = self.font,
                         bkg = bg)
                msg_rect.y += size - 2





