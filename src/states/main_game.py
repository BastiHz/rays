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
        self.raycaster = src.ray.RayCaster(
            self.rect.width // 2,
            self.rect.height // 2,
            math.pi,
            data
        )
        self.raycaster.make_new_rays(self.rect.width)

        self.walls = [
            src.wall.Wall(0, 0, 800, 0),  # top
            src.wall.Wall(0, 0, 0, 600),  # left
            src.wall.Wall(800, 0, 800, 600),  # right
            src.wall.Wall(0, 600, 800, 600),  # bottom
            # cube:
            src.wall.Wall(100, 75, 100, 150, (0, 255, 255)),
            src.wall.Wall(100, 150, 175, 150, (0, 0, 255)),
            src.wall.Wall(175, 150, 175, 75, (255, 0, 255)),
            src.wall.Wall(175, 75, 100, 75, (255, 255, 0)),
            # triangle:
            src.wall.Wall(200, 250, 250, 350, (255, 128, 0)),
            src.wall.Wall(250, 350, 150, 350, (0, 255, 128)),
            src.wall.Wall(150, 350, 200, 250, (0, 128, 255)),
            # spiral:
            src.wall.Wall(300, 50, 375, 50, (128, 0, 128)),
            src.wall.Wall(375, 50, 375, 190, (255, 128, 255)),
            src.wall.Wall(300, 50, 300, 125, (128, 255, 255)),
            src.wall.Wall(300, 125, 340, 125, (128, 0, 255)),
            src.wall.Wall(340, 125, 340, 80, (0, 255, 128)),
            src.wall.Wall(375, 190, 300, 190, (128, 128, 255))
        ]

    def start(self, data):
        super().start(data)
        pg.mouse.set_visible(False)

    def close(self):
        pg.mouse.set_visible(True)
        return super().close()

    def process_events(self, events, pressed, dt):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.done = True
                    return
        if pressed[pg.K_w]:
            self.raycaster.move(dt, 1)
        if pressed[pg.K_s]:
            self.raycaster.move(dt, -1)
        if pressed[pg.K_e]:
            self.raycaster.turn(dt, 1)
        if pressed[pg.K_q]:
            self.raycaster.turn(dt, -1)
        if pressed[pg.K_a]:
            self.raycaster.strafe(dt, -1)
        if pressed[pg.K_d]:
            self.raycaster.strafe(dt, 1)

    def update(self, dt):
        self.raycaster.update(dt, self.walls)

    def draw(self, window):
        window.fill(self.background_color)
        self.raycaster.draw_front_view(window, self.rect.height // 2)
