import pygame as pg
import os, sys
from typing import Tuple
import random as r
import math as m

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.menu.sprite.animated_sprite import *


class Player:
    def __init__(
        self,
        game,
        path: str,
        coords: Tuple[int, int],
        health: int,
        speed: int,
        animation_time: int,
        *args: str,
    ) -> None:
        self.game = game
        self.anim_dict = build_animation_dictionary(path, *args)
        self.health = health
        self.speed = speed
        self.x, self.y = coords

        self.selected_path = "walk"
        self.prev_anim_time = pg.time.get_ticks()
        self.animation_time = animation_time
        self.dead = False
        self.death_timer = 0
        self.death_flash = 0
        self.flip_check = False
        self.sprite = self.anim_dict[self.selected_path][0]
        self.h, self.w = self.sprite.get_height(), self.sprite.get_width()

        self.rect = pg.Rect(
            (
                self.x,
                self.y,
                self.anim_dict[self.selected_path][0].get_width() - 10,
                self.anim_dict[self.selected_path][0].get_height() - 10,
            )
        )

        self.position = (0, 0)
        self.attack_count = -1

    def input(self) -> None:
        keys = pg.key.get_pressed()
        dx, dy = self.x, self.y

        # Move up
        if (keys[pg.K_w] or keys[pg.K_UP]) and self.y > self.game.ui_manager.board.y:
            dy -= self.speed  # Move up based on speed
        # Move down
        if (keys[pg.K_s] or keys[pg.K_DOWN]) and self.y + self.anim_dict[
            self.selected_path
        ][
            0
        ].get_width() < self.game.ui_manager.board.y + self.game.ui_manager.board.sprite.get_height():
            dy += self.speed  # Move down based on speed
        # Move left
        if (keys[pg.K_a] or keys[pg.K_LEFT]) and self.x > self.game.ui_manager.board.x:
            dx -= self.speed  # Move left based on speed
            if not self.flip_check:
                self.flip_check = not self.flip_check

        # Move right
        if (keys[pg.K_d] or keys[pg.K_RIGHT]) and self.x + self.anim_dict[
            self.selected_path
        ][
            0
        ].get_height() < self.game.ui_manager.board.x + self.game.ui_manager.board.sprite.get_width():
            dx += self.speed  # Move right based on speed
            if self.flip_check:
                self.flip_check = not self.flip_check

        self.rect.x, self.rect.y = dx, dy
        if (
            self.game.coral_manager.check_collision(self.rect) != -1
            or self.rect.colliderect(self.game.house.rect)
            or self.game.squirrel_manager.check_collision(self.rect) != -1
        ):
            self.rect.x, self.rect.y = self.x, self.y
        else:
            self.x, self.y = dx, dy

    def update_health(self, val: int) -> None:
        self.health += val

    def death(self) -> None:
        death_sounds = [7, 11, 15, 22]
        self.game.sound_manager.play_sound(f"FishDeath_{death_sounds[r.randint(0, 3)]}")
        self.game.map[self.position[0]][self.position[1]].occupied = False
        self.game.map[self.position[0]][self.position[1]].occupant = None
        self.x, self.y = (self.game.house.x, self.game.house.y - 64)
        self.dead = True
        self.death_timer = 120
        self.death_flash = 180
        self.game.ui_manager.life_list.pop()
        self.game.coral_toggle = False

    def check_coral_valid(self, pos: Tuple[int, int]) -> bool:
        if (
            pos[0] < self.game.map[self.position[0] - 1][self.position[1]].x
            or pos[0]
            > self.game.map[self.position[0] + 1][self.position[1]].x
            + self.game.map[self.position[0] + 1][self.position[1]].w
            or pos[1] < self.game.map[self.position[0]][self.position[1] - 1].y
            or pos[1]
            > self.game.map[self.position[0]][self.position[1] + 1].y
            + self.game.map[self.position[0]][self.position[1] + 1].h
            or self.rect.collidepoint(pos)
        ):
            return False
        return True

    def draw_valid_boxes(self) -> None:
        for i in range(self.position[0] - 1, self.position[0] + 2):
            for j in range(self.position[1] - 1, self.position[1] + 2):
                if (
                    (i == self.position[0] and j == self.position[1])
                    or i <= -1
                    or j <= -1
                    or i >= 11
                    or j >= 11
                    or self.game.map[i][j].occupied
                ):
                    continue

                s = pg.Surface((self.game.map[i][j].w, self.game.map[i][j].h))
                s.fill("green")
                s.set_alpha(150)

                self.game.screen.screen.blit(
                    s, (self.game.map[i][j].x, self.game.map[i][j].y)
                )

    def update(self) -> None:
        if self.dead:
            self.death_timer -= 1
            if self.death_timer == 0:
                self.dead = False
            return
        self.input()
        if check_animation_time(self.animation_time, self.prev_anim_time):
            self.prev_anim_time = pg.time.get_ticks()
            animate(
                self.anim_dict,
                self.selected_path,
                self.game.screen.screen,
                (self.x, self.y),
            )

            if self.selected_path == "attack":
                self.attack_count -= 1

        if self.death_flash % 5 != 0 or self.death_flash == 0:
            self.sprite = self.anim_dict[self.selected_path][0]

            if self.flip_check:
                self.sprite = pg.transform.flip(self.sprite, True, False)

            self.game.screen.screen.blit(self.sprite, (self.x, self.y))
        prev_min_loc = float("inf")
        self.game.map[self.position[0]][self.position[1]].occupied = False
        self.game.map[self.position[0]][self.position[1]].occupant = None
        for k, i in enumerate(self.game.map):
            for l, j in enumerate(i):
                distance = m.sqrt(
                    (self.x + self.w / 2 - j.x + j.w / 2) ** 2
                    + (self.y + self.h / 2 - j.y + j.h / 2) ** 2
                )

                if distance < prev_min_loc:
                    self.position = (k - 1, l - 1)
                    prev_min_loc = distance
        self.game.map[self.position[0]][self.position[1]].occupied = True
        self.game.map[self.position[0]][self.position[1]].occupant = self

        if self.game.coral_toggle and not self.dead:
            self.draw_valid_boxes()

        if self.death_flash > 0:
            self.death_flash -= 1
        if self.health <= 0:
            self.health = 10
            self.death()

        if self.attack_count == 0:
            self.selected_path = "walk"
