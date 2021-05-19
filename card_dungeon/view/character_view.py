import card_dungeon.model as model
from .graphics import *
from .view import *


class CharacterView(View):
    MODE_PORTRAIT = "Portrait Mode"
    MODE_STATS = "Stats Mode"

    def __init__(self, name: str, width: int, height: int):
        super().__init__(name=name, width=width, height=height)
        self.model = None
        self.surface = None
        self.portrait_img = None

        self.mode = CharacterView.MODE_PORTRAIT
        self.is_highlighted = False
        self.bg = Colours.WHITE
        self.fg = Colours.DARK_GREEN

    def initialise(self, character: model.BaseCharacter):
        self.model = character
        self.surface = pygame.Surface((self.width, self.height))
        portrait = self.model.gender == model.Gender.FEMALE
        self.portrait_img = View.IMAGE_MANAGER.get_skin_image(tile_name=self.model.type, tick=portrait)

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
        header_rect = pygame.Rect(border.x, border.y, border.width, size)
        pygame.draw.rect(self.surface,
                         fg,
                         header_rect)

        if self.model is None:
            return

        msg = f"{self.model.name} the {self.model.type.value}"
        draw_text(self.surface, msg, x, y,
                  size=size,
                  fg_colour=self.bg,
                  bg_colour=self.fg)


        # Draw current health
        y += 14
        padding = 4
        heart_img = View.IMAGE_MANAGER.get_skin_image(tile_name=model.CharacterFeature.HEALTH, width=20, height=20)
        img_rect = heart_img.get_rect()

        start_x = x = 12
        for i in range(self.model.health):
            # 8 hearts per row.
            if i > 0 and i % 8 == 0:
                y += img_rect.height + padding
                x = start_x
            self.surface.blit(heart_img, (x, y))
            x += img_rect.width + 2

        temp_y = y + img_rect.height + padding

        if self.mode == CharacterView.MODE_PORTRAIT:
            # Draw the image of the character
            img = self.portrait_img
            img_rect = img.get_rect()
            img_rect.centerx = pane_rect.centerx
            img_rect.bottom = pane_rect.bottom - 16
            self.surface.blit(img, img_rect)

        elif self.mode == CharacterView.MODE_STATS:
            # Draw character stats
            x = pane_rect.centerx
            y += heart_img.get_rect().height + 20
            size = 16

            msg = f"Gender:{self.model.gender.value.title()}"
            draw_text(self.surface, msg, x, y,
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            y += size

            msg = f"Level:{self.model.level}"
            draw_text(self.surface, msg, x, y,
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            y += size

            msg = f"Rounds:{self.model.rounds}"
            draw_text(self.surface, msg, x, y,
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)
            y += size

            msg = f"Wins:{self.model.wins}"
            draw_text(self.surface, msg, x, y,
                      size=size,
                      fg_colour=self.fg,
                      bg_colour=self.bg)

        # Is the character dead?
        if self.model.is_dead:
            x, y = pane_rect.center
            size = 40
            msg = "*** DEAD ***"
            draw_text(self.surface,
                      msg,
                      x, y,
                      size=size,
                      fg_colour=self.bg,
                      bg_colour=self.fg)

        # Draw the current active effects
        y = temp_y
        x = 10
        size = 18

        for k, v in self.model.effects.items():
            img = View.IMAGE_MANAGER.get_skin_image(tile_name=k)
            img_rect = img.get_rect()
            img_rect.topleft = (x, y)
            self.surface.blit(img, img_rect)
            msg = f" {v} "
            draw_text(self.surface,
                      msg,
                      img_rect.left + 4,
                      img_rect.bottom,
                      size=size,
                      fg_colour=self.bg,
                      bg_colour=self.fg)

            x += img_rect.width + padding

    def on_click_zone(self, zone_name:str):
        # Don't care where the user clicked.
        # Toggle the View mode between character's portrait and character's stats
        if self.mode == CharacterView.MODE_PORTRAIT:
            self.mode = CharacterView.MODE_STATS
        elif self.mode == CharacterView.MODE_STATS:
            self.mode = CharacterView.MODE_PORTRAIT
