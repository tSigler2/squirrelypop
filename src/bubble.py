import pygame as pg
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib.sprite.animated_sprite import *

import random as r
from typing import Tuple


class Bubble:
    def __init__(self, game, path: str, *args: str) -> None:
        self.game = game
        self.anim_dict = build_animation_dictionary(path, *args)
        self.set_pos()
        self.animation_time = 120
        self.selected_path = "std"
        self.prev_animation_time = pg.time.get_ticks()
        self.pop_count = 0

        self.rect = pg.Rect(
            (
                self.x,
                self.y,
                self.anim_dict[self.selected_path][0].get_width(),
                self.anim_dict[self.selected_path][0].get_height(),
            )
        )

    def set_pos(self) -> None:
        self.x = r.randint(5, 1275)
        self.dy = r.randint(1, 2)
        self.y = r.randint(1281, 1381)

    def move(self) -> None:
        self.y -= self.dy

        if self.y <= -45:
            self.set_pos()

        self.rect.x, self.rect.y = self.x, self.y

    def check_collision(self, mouse_click: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_click)

    def update(self) -> None:
        self.move()

        if check_animation_time(self.animation_time, self.prev_animation_time):
            self.prev_animation_time = pg.time.get_ticks()
            animate(
                self.anim_dict,
                self.selected_path,
                self.game.screen.screen,
                (self.x, self.y),
            )

            if self.selected_path == "pop":
                self.pop_count += 1

        self.game.screen.screen.blit(
            self.anim_dict[self.selected_path][0], (self.x, self.y)
        )

        if (
            self.selected_path == "pop"
            and self.pop_count == len(self.anim_dict[self.selected_path]) - 1
        ):
            self.pop_count = 0
            self.anim_dict[self.selected_path].rotate(-1)
            self.selected_path = "std"
            self.set_pos()

            self.game.ui_manager.name_queue.put((self.x, self.y))
