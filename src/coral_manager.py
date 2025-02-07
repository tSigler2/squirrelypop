import pygame as pg

from coral import Coral
from typing import Tuple


class CoralManager:
    def __init__(self, game) -> None:
        self.game = game
        self.coral_list = []

    def add_coral(self, coords: Tuple[int, int]) -> None:
        self.coral_list.append(
            Coral(
                self.game,
                "assets/coral",
                (
                    self.game.map[coords[0]][coords[1]].x,
                    self.game.map[coords[0]][coords[1]].y,
                ),
                5,
                1,
                120,
                coords,
                120,
                "std",
            )
        )

        self.game.map[coords[0]][coords[1]].occupied = True
        self.game.map[coords[0]][coords[1]].occupant = self.coral_list[-1]
        self.game.money -= 5

    def update(self) -> None:
        destroy_list = []
        for i, coral in enumerate(self.coral_list):
            coral.update()
            if coral.health <= 0:
                destroy_list.append(i)

        for i in destroy_list:
            self.game.map[self.coral_list[i].coords[0]][
                self.coral_list[i].coords[1]
            ].occupied = False
            self.game.map[self.coral_list[i].coords[0]][
                self.coral_list[i].coords[1]
            ].occupant = None

            self.coral_list.pop(i)

    def check_collision(self, rect: pg.Rect) -> int:
        return rect.collidelist([coral.rect for coral in self.coral_list])
