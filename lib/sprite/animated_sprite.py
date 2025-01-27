import pygame as pg
from typing import Dict, Tuple, Protocol
from collections import deque
import os


class DrawableScreen(Protocol):
    screen: pg.Surface


def build_animation_dictionary(
    path: str,
    *args: Tuple[str, ...],
    resize: Tuple[bool, Tuple[int, int]] = (False, (0, 0))
) -> Dict[str, deque]:
    data_dict = {}

    for data in args:
        data_dict[data] = deque()

        full_path = os.path.join(path, data)

        for img in sorted(os.listdir(full_path)):
            data_dict[data].append(
                pg.image.load(os.path.join(full_path, img)).convert_alpha()
            )
            if resize[0]:
                data_dict[data][-1] = pg.transform.scale(data_dict[data][-1], resize[1])
    return data_dict


def check_animation_time(animation_time: int, prev_anim_time: int) -> bool:
    curr_time = pg.time.get_ticks()

    if curr_time - prev_anim_time >= animation_time:
        return True
    return False


def animate(
    data_dict: Dict[str, deque],
    selected_path: str,
    pg_screen: DrawableScreen,
    coords: Tuple[int, int],
) -> None:
    data_dict[selected_path].rotate(-1)
