from typing import Dict
import json

import pygame

from src.constants import DEFAULT_OPTIONS


images = {}
worlds = {}
options = {}
controls = {}


def load_images() -> None:
    pass


def load_worlds() -> None:
    pass


def load_options() -> None:
    try:
        with open("options.json", "r") as file:
            options.update(json.load(file))
    except FileNotFoundError:
        options.update(DEFAULT_OPTIONS)
        save_options()


def save_options() -> None:
    with open("options.json", "w") as file:
        json.dump(options, file, indent=4, sort_keys=True)


def load_controls() -> None:
    for k, v in options["controls"].items():
        controls[k] = pygame.key.key_code(v)


def load_all() -> None:
    load_options()
    load_controls()
    load_images()
    load_worlds()
