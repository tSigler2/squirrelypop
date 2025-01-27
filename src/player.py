import pygame as pg
import os, sys
from typing import Tuple
import random as r

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.sprite.animated_sprite import *


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

        self.rect = pg.Rect(
            (
                self.x,
                self.y,
                self.anim_dict[self.selected_path][0].get_width(),
                self.anim_dict[self.selected_path][0].get_height(),
            )
        )

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
        # Move right
        if (keys[pg.K_d] or keys[pg.K_RIGHT]) and self.x + self.anim_dict[
            self.selected_path
        ][
            0
        ].get_height() < self.game.ui_manager.board.x + self.game.ui_manager.board.sprite.get_width():
            dx += self.speed  # Move right based on speed

        self.rect.x, self.rect.y = dx, dy
        if self.game.coral_manager.check_collision(
            self.rect
        ) != -1 or self.rect.colliderect(self.game.house.rect):
            self.rect.x, self.rect.y = self.x, self.y
        else:
            self.x, self.y = dx, dy

        if keys[pg.K_j]:
            self.health = 0

    def update_health(self, val: int) -> None:
        self.health += val

    def death(self) -> None:
        death_sounds = [7, 11, 15, 22]
        self.game.sound_manager.play_sound(f"FishDeath_{death_sounds[r.randint(0, 3)]}")
        self.x, self.y = (self.game.house.x, self.game.house.y - 64)
        self.dead = True
        self.death_timer = 120
        self.death_flash = 180
        self.game.ui_manager.life_list.pop()

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
        if self.death_flash % 5 != 0 or self.death_flash == 0:
            self.game.screen.screen.blit(
                self.anim_dict[self.selected_path][0], (self.x, self.y)
            )

        if self.death_flash > 0:
            self.death_flash -= 1
        if self.health <= 0:
            self.health = 10
            self.death()
