import pygame as pg
from typing import Tuple, List


class Space:
    def __init__(self, coords: Tuple[int, int, int, int]) -> None:
        self.rect = pg.Rect(coords)
        self.x, self.y, self.w, self.h = coords
        self.occupied = False

    def check_collision(self, mouse_pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)


def gen_map() -> List[Space]:
    map = [
        [
            Space(
                (
                    int(600 / 11) * i + 640,
                    int(600 / 11) * j + 100,
                    int(600 / 11),
                    int(600 / 11),
                )
            )
            for j in range(11)
        ]
        for i in range(11)
    ]
    map[6][6].occupied = True

    return map
