import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame as pg

import src.resources
import src.states.state
import src.states.main_game


def run():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pg.init()
    config = src.resources.load_config()
    window = pg.display.set_mode((
        config["app"]["window_width"],
        config["app"]["window_height"]
    ))

    data = {"config": config}
    states = {
        "MainGame": src.states.main_game.Main(data),
    }
    state = states[config["app"]["start_state"]]
    state.start({})

    fps = config["app"]["fps"]
    clock = pg.time.Clock()
    while True:
        dt = clock.tick(fps) / 1000
        if pg.event.get(pg.QUIT):
            state.done = True
        else:
            state.process_events(pg.event.get(), pg.key.get_pressed(), dt)
        if state.done:
            state_data = state.close()
            if state_data["next_state_name"] == "quit":
                break
            state = states[state_data["next_state_name"]]
            state.start(state_data)
        state.update(dt)
        state.draw(window)
        pg.display.update()
