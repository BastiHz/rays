"""Manage resources:
load default config
save user defined config (if applicable)
load images, sounds, levels, etc.
load and save savegames etc
"""

import json


def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)
    return config


def load_images():
    pass


def load_sounds():
    pass


def load_levels():
    pass


def define_fonts():
    pass


def load_data():
    data = {
        "config": load_config(),
        "images": load_images(),
        "sounds": load_sounds(),
        "levels": load_levels(),
        "fonts": define_fonts()
    }
    return data
