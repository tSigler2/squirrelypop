import pygame as pg
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib.sprite.animated_sprite import *

from typing import Tuple


class Coral:
    def __init__(
        self,
        game,
        path: str,
        coords: Tuple[int, int],
        health: int,
        damage: int,
        animation_time: int,
        *args: str
    ) -> None:
        self.game = game
        self.anim_dict = build_animation_dictionary(
            path, *args, resize=(True, (50, 50))
        )
        self.health = health
        self.damage = damage
        self.animation_time = animation_time
        self.prev_anim_time = pg.time.get_ticks()
        self.selected_path = "std"

        self.x, self.y = coords
        self.w, self.h = (
            self.anim_dict[self.selected_path][0].get_width(),
            self.anim_dict[self.selected_path][0].get_height(),
        )

        self.rect = pg.Rect((self.x, self.y, self.w, self.h))

    def update(self) -> None:
        if check_animation_time(self.animation_time, self.prev_anim_time):
            self.prev_anim_time = pg.time.get_ticks()
            animate(
                self.anim_dict,
                self.selected_path,
                self.game.screen.screen,
                (self.x, self.y),
            )
        self.game.screen.screen.blit(
            self.anim_dict[self.selected_path][0], (self.x, self.y)
        )
