import pygame as pg
from typing import Tuple


class StaticSprite:
    def __init__(self, path: str, position: tuple[int, int]) -> None:
        self.path = path
        self.x, self.y = position

        self.sprite = pg.image.load(path).convert_alpha()
