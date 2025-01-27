import pygame as pg
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bubble import Bubble
from life_sprite import LifeSprite

from lib.menu.button import Button
from lib.sprite.static_sprite import StaticSprite
from lib.screen.background import Background
from typing import Tuple


class UIManager:
    def __init__(self, game) -> None:
        pg.font.init()
        self.game = game

        font_path = pg.font.match_font("arial")
        self.font = pg.font.Font(font_path, 72)
        self.font_color = (255, 255, 255)

        self.life_list = [
            LifeSprite(
                self.game, "assets/ui/SharkLife.png", (80, 0), (140, 180), 20, 60
            ),
            LifeSprite(
                self.game, "assets/ui/SharkLife.png", (80, 0), (290, 330), 20, 60
            ),
            LifeSprite(
                self.game, "assets/ui/SharkLife.png", (80, 0), (450, 490), 20, 60
            ),
            LifeSprite(
                self.game, "assets/ui/SharkLife.png", (500, 0), (140, 180), 20, 60
            ),
            LifeSprite(
                self.game, "assets/ui/SharkLife.png", (500, 0), (290, 330), 20, 60
            ),
            LifeSprite(
                self.game, "assets/ui/SharkLife.png", (500, 0), (450, 490), 20, 60
            ),
        ]

        self.start = Button(
            "assets/ui/buttons/StartButton.png", (540, 380), event=pg.USEREVENT + 22
        )
        self.settings = Button(
            "assets/ui/buttons/SettingsButton.png", (567, 440), event=pg.USEREVENT + 23
        )
        self.quit = Button(
            "assets/ui/buttons/QuitButton.png", (522, 500), event=pg.QUIT
        )
        self.banner = StaticSprite("assets/ui/logo.png", (400, 20))
        self.banner.sprite = pg.transform.scale(self.banner.sprite, (480, 320))
        self.background = Background("assets/ui/background.png", (0, 0, 1280, 720))

        self.bubbles = [Bubble("assets/ui/bubble.png", (0, 0)) for k in range(7)]

        self.board = StaticSprite("assets/ui/SandGrid.png", (640, 100))
        self.board.sprite = pg.transform.scale(self.board.sprite, (600, 600))

        self.num_display = StaticSprite("assets/ui/FE_Health_Counter.png", (200, 0))
        self.num_display.sprite = pg.transform.scale(
            self.num_display.sprite, (300, 600)
        )

        self.coral_button = Button(
            "assets/ui/buttons/PlaceCoralButton.png",
            (200, 230),
            event=pg.USEREVENT + 24,
        )
        self.coral_button.sprite = pg.transform.scale(
            self.coral_button.sprite, (300, 150)
        )
        self.coral_button.rect = pg.Rect(
            self.coral_button.x, self.coral_button.y, 300, 150
        )

    def update(self):
        self.game.screen.screen.blit(
            self.background.background, (self.background.x, self.background.y)
        )

        mouse_pos = pg.mouse.get_pos()
        for bubble in self.bubbles:
            bubble.move()
            self.game.screen.screen.blit(bubble.sprite, (bubble.x, bubble.y))

        if self.game.mode == "start_menu":

            self.start.sprite.set_alpha(255)
            self.settings.sprite.set_alpha(255)
            self.quit.sprite.set_alpha(255)

            if self.start.check_press(mouse_pos):
                self.start.sprite.set_alpha(200)
            if self.settings.check_press(mouse_pos):
                self.settings.sprite.set_alpha(200)
            if self.quit.check_press(mouse_pos):
                self.quit.sprite.set_alpha(200)

            self.game.screen.screen.blit(
                self.start.sprite, (self.start.x, self.start.y)
            )
            self.game.screen.screen.blit(
                self.settings.sprite, (self.settings.x, self.settings.y)
            )
            self.game.screen.screen.blit(self.quit.sprite, (self.quit.x, self.quit.y))
            self.game.screen.screen.blit(
                self.banner.sprite, (self.banner.x, self.banner.y)
            )
        elif self.game.mode == "settings":
            pass
        elif self.game.mode == "game":
            self.game.screen.screen.blit(
                self.board.sprite, (self.board.x, self.board.y)
            )

            self.game.screen.screen.blit(
                self.num_display.sprite, (self.num_display.x, self.num_display.y)
            )

            self.coral_button.sprite.set_alpha(255)
            if self.coral_button.check_press(mouse_pos):
                self.coral_button.sprite.set_alpha(200)

            self.game.screen.screen.blit(
                self.coral_button.sprite, (self.coral_button.x, self.coral_button.y)
            )

            money_surface = self.font.render(
                f"{self.game.money}", True, self.font_color
            )
            life_surface = self.font.render(
                f"{self.game.player.health}", True, self.font_color
            )
            self.game.screen.screen.blit(money_surface, (340, 70))
            self.game.screen.screen.blit(life_surface, (400, 465))
            for life in self.life_list:
                life.update()

    def check_events(self):
        mouse_pos = pg.mouse.get_pos()
        if self.game.mode == "start_menu":
            if self.quit.check_press(mouse_pos):
                self.quit.activate_event()
            if self.start.check_press(mouse_pos):
                self.start.activate_event()
            if self.settings.check_press(mouse_pos):
                self.settings.activate_event()

        elif self.game.mode == "game":
            if self.coral_button.check_press(mouse_pos) and not self.game.coral_toggle:
                self.coral_button.activate_event()
