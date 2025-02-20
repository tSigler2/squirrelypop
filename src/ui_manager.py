import pygame as pg
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bubble import Bubble
from life_sprite import LifeSprite

from lib.menu.button import Button
from lib.menu.sprite.static_sprite import StaticSprite
from lib.screen.background import Background
from typing import Tuple
import random as r
from queue import Queue

name_list = [
    "Jean-Alexei Hernandez",
    "David Jones",
    "Sagar Patel",
    "Thomas Sigler",
    "Jake Hitchcock",
    "Stephen Schaad",
    "Nneka Otuonye",
    "Alireza Asni-Ashari",
    "Sohum Honavar",
    "Thomas Vu",
    "Laura Baptie",
    "Ella Ortega",
    "Sam Soard",
    "Carome Taylor",
    "Kilee Turner",
    "Howard Wood",
]

NAME_MAX_LENGTH = 300


class UIManager:
    def __init__(self, game) -> None:
        pg.font.init()
        self.game = game

        self.font = pg.font.Font("squirrelypop/assets/ui/font.ttf", 72)
        self.font_color = (255, 255, 255)
        self.name_queue = Queue()
        self.name_list = []

        self.life_list = [
            LifeSprite(
                self.game, "squirrelypop/assets/ui/SharkLife.png", (80, 0), (140, 180), 20, 60
            ),
            LifeSprite(
                self.game, "squirrelypop/assets/ui/SharkLife.png", (80, 0), (290, 330), 20, 60
            ),
            LifeSprite(
                self.game, "squirrelypop/assets/ui/SharkLife.png", (80, 0), (450, 490), 20, 60
            ),
            LifeSprite(
                self.game, "squirrelypop/assets/ui/SharkLife.png", (500, 0), (140, 180), 20, 60
            ),
            LifeSprite(
                self.game, "squirrelypop/assets/ui/SharkLife.png", (500, 0), (290, 330), 20, 60
            ),
            LifeSprite(
                self.game, "squirrelypop/assets/ui/SharkLife.png", (500, 0), (450, 490), 20, 60
            ),
        ]

        self.volume_list = [
            [
                pg.Surface((20, int(pg.math.lerp(20, 100, i / 10)))),
                (
                    int(pg.math.lerp(400, 800, i / 10)),
                    int(200 - pg.math.lerp(20, 100, i / 10)),
                ),
            ]
            for i in range(1, 11)
        ]

        for surface in self.volume_list:
            surface[0].fill("green")

        self.start = Button(
            "squirrelypop/assets/ui/buttons/StartButton.png", (540, 380), event=pg.USEREVENT + 22
        )
        self.settings = Button(
            "squirrelypop/assets/ui/buttons/SettingsButton.png", (567, 440), event=pg.USEREVENT + 23
        )
        self.quit = Button(
            "squirrelypop/assets/ui/buttons/QuitButton.png", (522, 500), event=pg.QUIT
        )

        self.options_leave = Button(
            "squirrelypop/assets/ui/buttons/exit_options.png", (520, 600), event=pg.USEREVENT + 27
        )

        self.banner = StaticSprite("squirrelypop/assets/ui/logo.png", (400, 20))
        self.banner.sprite = pg.transform.scale(self.banner.sprite, (480, 320))
        self.background = Background("squirrelypop/assets/ui/background.png", (0, 0, 1280, 720))

        self.bubbles = [
            Bubble(self.game, "squirrelypop/assets/ui/bubble", "std", "pop") for k in range(7)
        ]

        self.board = StaticSprite("squirrelypop/assets/ui/SandGrid.png", (640, 100))
        self.board.sprite = pg.transform.scale(self.board.sprite, (600, 600))

        self.num_display = StaticSprite("squirrelypop/assets/ui/FE_Health_Counter.png", (200, 0))
        self.num_display.sprite = pg.transform.scale(
            self.num_display.sprite, (300, 600)
        )

        self.coral_button = Button(
            "squirrelypop/assets/ui/buttons/PlaceCoralButton.png",
            (200, 230),
            event=pg.USEREVENT + 24,
        )
        self.coral_button.sprite = pg.transform.scale(
            self.coral_button.sprite, (300, 150)
        )
        self.coral_button.rect = pg.Rect(
            self.coral_button.x, self.coral_button.y, 300, 150
        )

        self.name_list = []

    def update(self) -> None:
        self.game.screen.screen.blit(
            self.background.background, (self.background.x, self.background.y)
        )

        mouse_pos = pg.mouse.get_pos()
        for bubble in self.bubbles:
            bubble.update()

        if self.game.mode == "start_menu":
            name_death = []
            self.start.sprite.set_alpha(255)
            self.settings.sprite.set_alpha(255)
            self.quit.sprite.set_alpha(255)

            if self.start.check_press(mouse_pos):
                self.start.sprite.set_alpha(200)
            if self.settings.check_press(mouse_pos):
                self.settings.sprite.set_alpha(200)
            if self.quit.check_press(mouse_pos):
                self.quit.sprite.set_alpha(200)

            if not self.name_queue.empty():
                count = self.name_queue.qsize()
                for k in range(count):
                    self.name_list.append(
                        [
                            self.font.render(
                                name_list[r.randint(0, len(name_list) - 1)],
                                True,
                                self.font_color,
                            ),
                            self.name_queue.get(),
                            300,
                        ]
                    )
                    self.name_list[-1][0] = pg.transform.scale(
                        self.name_list[-1][0],
                        (
                            int(self.name_list[-1][0].get_width() * 0.50),
                            int(self.name_list[-1][0].get_height() * 0.50),
                        ),
                    )

            death_list = []

            for k, name in enumerate(self.name_list):
                if name[2] == 0:
                    death_list.append(k)

                self.game.screen.screen.blit(name[0], name[1])
                name[2] -= 1

                name[0].set_alpha(((name[2] / NAME_MAX_LENGTH) * 255))

            for i in death_list:
                self.name_list.pop(i)

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
            vol_surface = self.font.render("Volume", True, self.font_color)

            self.game.screen.screen.blit(vol_surface, (520, 20))

            for i in range(len(self.volume_list)):
                self.game.screen.screen.blit(
                    self.volume_list[i][0], self.volume_list[i][1]
                )
            self.game.screen.screen.blit(
                self.options_leave.sprite, (self.options_leave.x, self.options_leave.y)
            )
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

        elif self.game.mode == "settings" and pg.mouse.get_pressed()[0]:
            vol_num = 10
            change_vol = False
            for idx, i in enumerate(self.volume_list):
                if (
                    i[0]
                    .get_rect(
                        center=(
                            int(i[1][0] + i[0].get_width() / 2),
                            int(i[1][1] + i[0].get_height() / 2),
                        )
                    )
                    .collidepoint(mouse_pos)
                ):
                    vol_num = idx
                    change_vol = True
                    break
            if change_vol:
                for k in range(len(self.volume_list)):
                    if k <= vol_num:
                        self.volume_list[k][0].fill("green")
                    else:
                        self.volume_list[k][0].fill("red")

                pg.mixer.music.set_volume(vol_num / 10)

                if vol_num == 1:
                    pg.mixer.music.set_volume(0.0)
            if self.options_leave.check_press(mouse_pos):
                self.options_leave.activate_event()

        elif self.game.mode == "game":
            if self.coral_button.check_press(mouse_pos) and not self.game.coral_toggle:
                self.coral_button.activate_event()
