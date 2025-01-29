import pygame as pg
import os, sys
import random as r

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib.sprite.animated_sprite import *

from typing import Tuple


class Squirrel:
    def __init__(
        self, game, path: str, health: int, damage: int, animation_time: int, *args: str
    ) -> None:
        self.game = game
        self.anim_dict = build_animation_dictionary(path, *args)
        self.health = health
        self.damage = damage
        self.animation_time = animation_time
        self.prev_anim_time = pg.time.get_ticks()

        if r.random() >= 0.5:
            columns = True
        else:
            columns = False

        if r.random() >= 0.5:
            side = True
        else:
            side = False

        square = r.randint(0, 11)

        if columns:
            if side:
                coords = (0, square)
            else:
                coords = (10, square)
        else:
            if side:
                coords = (square, 0)
            else:
                coords = (10, square)
        self.x, self.y = coords

    def bfs(self):
        pass

    def update(self):
        pass
