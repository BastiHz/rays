import math

import pygame as pg

from src.states.state import State
import src.ray
import src.wall


class Main(State):
    def __init__(self, data):
        super().__init__(data)
        self.rect = pg.display.get_surface().get_rect()
        self.background_color = data["config"]["background_color"]
        self.world = data["worlds"]["test_1"]
        self.raycaster = src.ray.RayCaster(
            self.world,
            data["config"]["RayCaster"]
        )
        self.raycaster.make_new_rays(self.rect.width)

        self.walls = [src.wall.Wall(*w) for w in self.world["walls"]]

    def start(self, data):
        super().start(data)

        # lock the mouse to the pygame window:
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

    def close(self):
        # release the mouse from the pygame window:
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)

        return super().close()

    def process_events(self, events, pressed, dt):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.done = True
                    return
            if e.type == pg.MOUSEMOTION:
                self.raycaster.turn_mouse(e.rel[0])
        if pressed[pg.K_w]:
            self.raycaster.move(dt, 1)
        if pressed[pg.K_s]:
            self.raycaster.move(dt, -1)
        if pressed[pg.K_e]:
            self.raycaster.turn_keyboard(dt, 1)
        if pressed[pg.K_q]:
            self.raycaster.turn_keyboard(dt, -1)
        if pressed[pg.K_a]:
            self.raycaster.strafe(dt, -1)
        if pressed[pg.K_d]:
            self.raycaster.strafe(dt, 1)

    def update(self, dt):
        self.raycaster.update(dt, self.walls)

    def draw(self, window):
        window.fill(self.background_color)
        self.raycaster.draw_front_view(window, self.rect.height // 2)
