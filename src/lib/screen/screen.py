import pygame as pg
import sys
from typing import Tuple, List


class Screen:
    def __init__(self, dims: Tuple[int, int], flags) -> None:
        pg.display.init()
        self.screen = pg.display.set_mode(size=dims, flags=flags)
        self.flags = flags
        self.dims = dims

        self.clock = pg.time.Clock()

    def events(self, e):
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if e.type == pg.VIDEORESIZE:
            self.toggle_fs()

    def toggle_fs(self):
        self.flags ^= pg.FULLSCREEN
        self.screen = pg.display.set_mode(size=self.dims, flags=self.flags)


if __name__ == "__main__":
    screen = Screen((450, 360), flags=pg.RESIZABLE)

    while True:
        for e in pg.event.get():
            screen.events(e)
