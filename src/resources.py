import json
import os

import pygame
import pygame.freetype
import numpy

from src.constants import *


images = {}
worlds = {}
options = {}
controls = {}
fonts = {}


def load_images():
    pass


def load_worlds():
    for filename in os.listdir("worlds"):
        with open(os.path.join("worlds", filename), "r") as file:
            world_data = json.load(file)
            world_name = os.path.splitext(filename)[0]
            world_data["map"] = numpy.asarray(world_data["map"], dtype=int)
            worlds[world_name] = world_data


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
    # TODO: Put this values into constants.py (font name, colors, size)
    dev_font = pygame.freetype.Font(
        os.path.join("fonts", "Inconsolata-VariableFont.ttf"),
        16
    )
    dev_font.fgcolor = (255, 255, 255)
    dev_font.bgcolor = (32, 32, 32)
    dev_font.pad = True
    fonts.update({"dev_font": dev_font})


def load_all():
    load_options()
    load_controls()
    load_images()
    load_worlds()
    load_fonts()
