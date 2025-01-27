import pygame as pg
from typing import Tuple
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sprite.static_sprite import StaticSprite
from sprite.animated_sprite import DrawableScreen


class Button(StaticSprite):
    def __init__(
        self, path: str, position: Tuple[int, int], event=pg.USEREVENT
    ) -> None:
        super().__init__(path, position)

        self.event = event

        self.rect = pg.Rect(
            self.x, self.y, self.sprite.get_width(), self.sprite.get_height()
        )

    def activate_event(self) -> None:
        pg.event.post(pg.event.Event(self.event))

    def check_press(self, coords: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(coords)
