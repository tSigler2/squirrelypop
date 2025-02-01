import pygame as pg
import os, sys
import random as r

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib.sprite.animated_sprite import *

from typing import Tuple, List
from collections import deque


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
        self.selected_path = "walk"

        if r.random() >= 0.5:
            columns = True
        else:
            columns = False

        if r.random() >= 0.5:
            side = True
        else:
            side = False

        square = r.randint(0, 10)

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
        self.position = coords

        self.x, self.y = (
            self.game.map[self.position[0]][self.position[1]].x,
            self.game.map[self.position[0]][self.position[1]].y,
        )

        self.path = self.bfs()
        print(self.path)

    def bfs(self) -> List[Tuple[int, int]]:
        q = deque([((self.position[0], self.position[1]), [])])

        dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        v = set((self.x, self.y))
        visited = set([(self.x, self.y)])

        while q:
            (x, y), path = q.popleft()

            if (
                self.game.map[x][y].occupied
                and type(self.game.map[x][y].occupant) is not Squirrel
            ):
                return path

            for dx, dy in dir:
                nx, ny = x + dx, y + dy

                if (
                    nx > -1
                    and nx < 11
                    and ny > -1
                    and ny < 11
                    and (nx, ny) not in visited
                ):
                    visited.add((nx, ny))
                    q.append(((nx, ny), path + [(nx, ny)]))
        return None

    def move(self):
        pass

    def update(self) -> None:
        if check_animation_time(self.animation_time, self.prev_anim_time):
            self.prev_animation_time = pg.time.get_ticks()
            animate(
                self.anim_dict,
                self.selected_path,
                self.game.screen.screen,
                (self.x, self.y),
            )

        self.game.screen.screen.blit(
            self.anim_dict[self.selected_path][0], (self.x, self.y)
        )
