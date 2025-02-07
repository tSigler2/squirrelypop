import pygame as pg
import sys, os
import random as r

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.menu.sprite.static_sprite import StaticSprite

from typing import Tuple


class LifeSprite(StaticSprite):
    def __init__(
        self,
        game,
        path: str,
        position: Tuple[int, int],
        bounds: Tuple[int, int],
        float_phases: int,
        delta_change: int,
    ) -> None:
        self.game = game

        super().__init__(path, position)
        self.sprite = pg.transform.scale(self.sprite, (128, 128))

        self.bounds = bounds
        self.float_phases = float_phases

        self.intervals = int((bounds[1] - bounds[0]) / self.float_phases)
        self.delta_change = delta_change
        self.last_time = pg.time.get_ticks()

        self.y = int(r.randint(0, self.intervals) * self.intervals + self.bounds[0])

        if r.random() >= 0.5:
            self.dir = True
        else:
            self.dir = False
        self.w, self.h = self.sprite.get_width(), self.sprite.get_height()

    def float_change(self) -> None:
        if r.random() > 0.8 and self.delta_change > 20:
            self.delta_change -= 1
        elif r.random() < 0.2 and self.delta_change < 60:
            self.delta_change += 1
        if self.y >= self.bounds[1] or self.y <= self.bounds[0]:
            self.dir = not self.dir

        if self.dir:
            self.y += int(self.intervals)
            return
        self.y -= int(self.intervals)

    def update(self) -> None:
        curr_time = pg.time.get_ticks()

        if (curr_time - self.last_time) >= self.delta_change:
            self.last_time = curr_time
            self.float_change()

        self.game.screen.screen.blit(self.sprite, (self.x, self.y))
