import json
import os

import pygame
import pygame.freetype

from src.constants import DEFAULT_OPTIONS


images = {}
worlds = {}
options = {}
controls = {}
fonts = {}


def load_images():
    pass


def load_worlds():
    pass


def load_options():
    try:
        with open("options.json", "r") as file:
            options.update(json.load(file))
    except FileNotFoundError:
        options.update(DEFAULT_OPTIONS)
        save_options()


def save_options():
    with open("options.json", "w") as file:
        json.dump(options, file, indent=4, sort_keys=True)


def load_controls():
    for k, v in options["controls"].items():
        controls[k] = pygame.key.key_code(v)


def load_fonts():
    dev_font = pygame.freetype.Font(
        os.path.join("fonts", "Inconsolata-VariableFont.ttf"),
        18
    )
    dev_font.fgcolor = (255, 255, 255)
    dev_font.pad = True
    fonts.update({"dev_font": dev_font})


def load_all():
    load_options()
    load_controls()
    load_images()
    load_worlds()
    load_fonts()
