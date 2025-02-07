import pygame as pg
import os
from typing import Tuple


class SoundManager:
    def __init__(self) -> None:

        pg.mixer.init()
        self.sound_dict = {}

    def add_sound(self, *args: str, path: str = None) -> None:
        for sound in args:
            if path is not None:
                full_path = os.path.join(path, sound)

            else:
                full_path = sound

            self.sound_dict[sound[:-4]] = pg.mixer.Sound(full_path)

    def play_sound(self, sound: str) -> None:
        try:
            self.sound_dict[sound].play()
        except Exception as e:
            print(f"Error Playing {sound} -- {e}")

    def music(self, opt: str, music: str = None) -> None:
        if opt == "play":
            pg.mixer.music.play(-1)

        elif opt == "load":
            try:
                pg.mixer.music.load(music)
            except Exception as e:
                print(f"Error Loading {music} -- {e}")

        elif opt == "unload":
            pg.mixer.music.unload()

        elif opt == "pause":
            pg.mixer.music.pause()

        elif opt == "unpause":
            pg.mixer.music.unpause()
