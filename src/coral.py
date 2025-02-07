import pygame as pg
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib.menu.sprite.animated_sprite import *

from typing import Tuple
from enemy import Squirrel


class Coral:
    def __init__(
        self,
        game,
        path: str,
        coords: Tuple[int, int],
        health: int,
        damage: int,
        animation_time: int,
        grid_position: Tuple[int, int],
        dam_delta: int,
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
        self.coords = grid_position
        self.x, self.y = coords
        self.w, self.h = (
            self.anim_dict[self.selected_path][0].get_width(),
            self.anim_dict[self.selected_path][0].get_height(),
        )

        self.rect = pg.Rect((self.x, self.y, self.w, self.h))
        self.dam_delta = dam_delta

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

        for i in range(self.coords[0] - 1, self.coords[0] + 2):
            for j in range(self.coords[1] - 1, self.coords[1] + 2):
                if i != j and self.game.map[i][j].occupied:
                    if type(self.game.map[i][j].occupant) == Squirrel:
                        self.game.map[i][j].occupant.health -= 1
