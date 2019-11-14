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


def define_fonts():
    pass
