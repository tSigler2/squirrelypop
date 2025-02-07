import pygame as pg
from typing import Tuple


class Background:
    def __init__(self, path: str, coords: Tuple[int, int, int, int]):
        self.path = path
        self.x, self.y, self.w, self.h = coords

        self.background = pg.image.load(path).convert_alpha()
        self.background = pg.transform.scale(self.background, (self.w, self.h))
