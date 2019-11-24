"""Manage resources:
load default config
save user defined config (if applicable)
load images, sounds, levels, etc.
load and save savegames etc
"""

import json
import os


def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)
    return config


def load_images():
    pass


def load_sounds():
    pass


def load_worlds():
    worlds = {}
    worlds_dir = "worlds"
    for filename in os.listdir(worlds_dir):
        world_name = os.path.splitext(filename)[0]
        with open(os.path.join(worlds_dir, filename), "r") as file:
            worlds[world_name] = json.load(file)
    return worlds


def define_fonts():
    pass


def load_data():
    data = {
        "config": load_config(),
        "images": load_images(),
        "sounds": load_sounds(),
        "worlds": load_worlds(),
        "fonts": define_fonts()
    }
    return data
