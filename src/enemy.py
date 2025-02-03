import pygame as pg
import os, sys
import random as r

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib.sprite.animated_sprite import *

from typing import Tuple, List
from collections import deque

MOVE_DELTA_MAX = 60


class Squirrel:
    def __init__(
        self,
        game,
        path: str,
        health: int,
        damage: int,
        animation_time: int,
        move_time: int,
        *args: str
    ) -> None:
        self.game = game
        self.anim_dict = build_animation_dictionary(path, *args)
        self.health = health
        self.damage = damage
        self.animation_time = animation_time
        self.prev_anim_time = pg.time.get_ticks()
        self.selected_path = "walk"
        self.move_time = move_time
        self.move_delta = 0
        self.prev_move_time = pg.time.get_ticks()
        self.attack_frames = 0
        self.sprite = self.anim_dict[self.selected_path][0]
        self.w, self.h = self.sprite.get_width(), self.sprite.get_height()

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
        self.rect = pg.Rect((self.x, self.y, self.w, self.h))

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
                    if type(self.game.map[nx][ny].occupant) is Squirrel:
                        continue
                    visited.add((nx, ny))
                    q.append(((nx, ny), path + [(nx, ny)]))
        return []

    def move(self):
        self.x, self.y = pg.math.lerp(
            self.x,
            self.game.map[self.path[0][0]][self.path[0][1]].x,
            self.move_delta / MOVE_DELTA_MAX,
        ), pg.math.lerp(
            self.y,
            self.game.map[self.path[0][0]][self.path[0][1]].y,
            self.move_delta / MOVE_DELTA_MAX,
        )
        self.move_delta += 1

        if self.move_delta == MOVE_DELTA_MAX:
            self.move_delta = 0
            self.prev_move_time = pg.time.get_ticks()
            self.game.map[self.position[0]][self.position[1]].occupant = None
            self.game.map[self.position[0]][self.position[1]].occupied = False

            self.position = self.path.pop(0)
            self.game.map[self.position[0]][self.position[1]].occupant = self
            self.game.map[self.position[0]][self.position[1]].occupied = True

    def attack(self, coords: Tuple[int, int]) -> None:
        if self.game.map[coords[0]][coords[1]].occupied:
            self.game.map[coords[0]][coords[1]].occupant.health -= 1
        if self.game.map[coords[0]][coords[1]].occupant.health >= 0:
            self.selected_path = "walk"
        self.attack_frames = 0

    def update(self) -> None:
        if self.path == []:
            self.path = self.bfs()
            if self.path == []:
                return
        if check_animation_time(self.animation_time, self.prev_anim_time):
            self.prev_animation_time = pg.time.get_ticks()
            animate(
                self.anim_dict,
                self.selected_path,
                self.game.screen.screen,
                (self.x, self.y),
            )
            self.sprite = self.anim_dict[self.selected_path][0]

            if self.selected_path == "attack":
                self.attack_frames += 1

        curr_tick = pg.time.get_ticks()
        check_flip = False
        if self.position[0] > 0:
            if self.path[0][0] < self.position[0]:
                self.sprite = pg.transform.flip(self.sprite, True, False)
                if self.selected_path == "attack":
                    self.game.screen.screen.blit(self.sprite, (self.x - self.w, self.y))
                elif self.selected_path == "walk":
                    self.game.screen.screen.blit(self.sprite, (self.x, self.y))

                check_flip = True

        if (curr_tick - self.prev_move_time) >= self.move_time and not self.game.map[
            self.path[0][0]
        ][self.path[0][1]].occupied:
            self.move()
        elif self.game.map[self.path[0][0]][self.path[0][1]].occupied:
            self.selected_path = "attack"

        if self.selected_path == "attack" and self.attack_frames == 13:
            self.attack((self.path[0][0], self.path[0][1]))
        if not check_flip:
            self.game.screen.screen.blit(self.sprite, (self.x, self.y))

        self.rect.x, self.rect.y = self.x, self.y
