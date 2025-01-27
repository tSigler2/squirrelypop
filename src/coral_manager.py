import pygame as pg

from coral import Coral
from typing import Tuple


class CoralManager:
    def __init__(self, game) -> None:
        self.game = game
        self.coral_list = []

    def add_coral(self, coords: Tuple[int, int]) -> None:
        self.coral_list.append(
            Coral(self.game, "assets/coral", coords, 5, 1, 120, "std")
        )

    def update(self) -> None:
        destroy_list = []
        for i, coral in enumerate(self.coral_list):
            coral.update()
            if coral.health <= 0:
                destroy_list.append(i)

        for i in destroy_list:
            self.coral_list.pop(i)

    def check_collision(self, rect: pg.Rect) -> bool:
        return rect.collidelist([coral.rect for coral in self.coral_list])
