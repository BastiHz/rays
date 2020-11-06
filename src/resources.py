import json

from src.constants import DEFAULT_OPTIONS


images = {}
worlds = {}
options = {}
controls = {}


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
    controls.update(options["controls"])


def save_options():
    with open("options.json", "w") as file:
        json.dump(options, file, indent=4, sort_keys=True)


def load_all():
    load_options()
    load_images()
    load_worlds()
