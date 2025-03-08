import pygame as pg
import os, sys
import random as r
import math as m

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Tuple
from enemy import Squirrel


class SquirrelManager:
    def __init__(self, game, start_rate: int, eval_rate: int) -> None:
        self.game = game
        self.squirrel_list = []
        self.spawn_tick = 0
        self.spawn_limit = start_rate
        self.start_rate = start_rate
        self.eval_rate = eval_rate
        self.start_tick = 0

    def spawn_squirrel(self) -> None:
        self.squirrel_list.append(
            Squirrel(self.game, "squirrelypop/assets/squirrel", 10, 1, 120, 300, "walk", "attack")
        )
        self.game.map[self.squirrel_list[-1].position[0]][
            self.squirrel_list[-1].position[1]
        ].occupied = True
        self.game.map[self.squirrel_list[-1].position[0]][
            self.squirrel_list[-1].position[1]
        ].occupant = self.squirrel_list[-1]

    def check_spawn(self) -> None:
        if self.spawn_tick > self.spawn_limit:
            self.spawn_tick = 0
            self.spawn_squirrel()

        if self.spawn_tick - self.start_tick <= self.start_rate:
            return

        self.spawn_limit = self.start_rate / (1 + m.log10(curr_tick / self.eval_rate))

    def check_collision(self, rect: pg.Rect) -> int:
        return rect.collidelist([enemy.rect for enemy in self.squirrel_list])

    def update(self) -> None:
        self.spawn_tick += 1
        self.check_spawn()
        death_list = []
        for i, squirrel in enumerate(self.squirrel_list):
            if squirrel.health <= 0:
                death_list.append(i)

            squirrel.update()

        for i in death_list:
            self.squirrel_list.pop(i)
