import pygame as pg
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib.menu.sprite.animated_sprite import *


class House:
    def __init__(
        self, game, path, position, health, money_delta, animation_time, *args
    ):
        self.game = game
        self.x, self.y = position
        self.anim_dict = build_animation_dictionary(path, *args)
        self.health = health
        self.money_delta = money_delta
        self.prev_money_delta = pg.time.get_ticks()
        self.selected_path = "std"
        self.prev_anim_time = pg.time.get_ticks()
        self.animation_time = animation_time
        self.death_count = -1

        self.rect = pg.Rect(
            (
                self.x,
                self.y,
                self.anim_dict[self.selected_path][0].get_width(),
                self.anim_dict[self.selected_path][0].get_height(),
            )
        )

    def update(self):
        curr_ticks = pg.time.get_ticks()

        if curr_ticks - self.prev_money_delta >= self.money_delta:
            self.prev_money_delta = curr_ticks
            self.game.money += 1

        if check_animation_time(self.animation_time, self.prev_anim_time):
            self.prev_anim_time = pg.time.get_ticks()
            animate(
                self.anim_dict,
                self.selected_path,
                self.game.screen.screen,
                (self.x, self.y),
            )
            if self.selected_path == "death":
                self.death_count -= 1
        self.game.screen.screen.blit(
            self.anim_dict[self.selected_path][0], (self.x, self.y)
        )

        if self.health <= 0 and self.death_count == -1:
            self.selected_path = "death"
            self.death_count = 4

        if self.death_count == 0:
            self.game.run_game = False
