import pygame as pg
import os, sys
from typing import Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.screen.screen import Screen
from lib.screen.background import Background
from ui_manager import UIManager
from lib.util.sound import SoundManager
from player import Player
from house import House
from coral_manager import CoralManager
from square import *


class Game:
    def __init__(self, dims: Tuple[int, int]) -> None:
        self.screen = Screen(dims, pg.RESIZABLE)
        self.clock = pg.time.Clock()

        self.ui_manager = UIManager(self)
        self.sound_manager = SoundManager()
        self.player = Player(
            self, "assets/player", (1000, 400), 10, 2, 120, "walk", "attack"
        )
        self.house = House(
            self, "assets/house", (910, 360), 10, 2400, 120, "std", "death"
        )
        self.map = gen_map()
        self.coral_manager = CoralManager(self)

        self.mode = "start_menu"
        self.coral_toggle = False

        self.money = 0

    def run(self) -> None:
        mouse_cool_down = 0
        self.sound_manager.music("load", "assets/sounds/TownTheme.mp3")
        self.sound_manager.music("play")

        self.sound_manager.add_sound(
            "FishDeath_7.wav",
            "FishDeath_11.wav",
            "FishDeath_15.wav",
            "FishDeath_22.wav",
            path="assets/player/FishDeathSounds",
        )

        while True:
            for e in pg.event.get():
                self.screen.events(e)

                if e.type == pg.USEREVENT + 22:
                    self.mode = "game"
                elif e.type == pg.USEREVENT + 23:
                    self.mode = "settings"
                elif e.type == pg.USEREVENT + 24:
                    self.coral_toggle = True
                    mouse_cool_down = 3
                    print("Can Place Coral")
            if mouse_cool_down > 0:
                mouse_cool_down -= 1
            if pg.mouse.get_pressed()[0]:
                self.ui_manager.check_events()
                if self.coral_toggle and mouse_cool_down == 0:
                    for row in self.map:
                        for space in row:
                            if space.check_collision(pg.mouse.get_pos()):
                                self.coral_manager.add_coral((space.x, space.y))
                                self.coral_toggle = False
                                break
                        if not self.coral_toggle:
                            break
                    self.coral_toggle = False
                print(self.coral_toggle)

            self.ui_manager.update()
            if self.mode == "game":
                self.player.update()
                self.house.update()
                self.coral_manager.update()
            pg.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game((1280, 720))
    game.run()
