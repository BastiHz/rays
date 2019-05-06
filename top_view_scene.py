import math
import pygame as pg
from ray import Ray
from wall import Wall


class TopView:
    def __init__(self, app):
        self.app = app
        self.ray_origin_pos = (0, 0)
        self.rays = []
        for a in range(0, 360, 10):
            print(a)
            self.rays.append(Ray(self.ray_origin_pos, math.radians(a)))
        self.walls = [
            Wall(600, 200, 500, 500),
            Wall(0, 0, 800, 0),
            Wall(0, 0, 0, 600),
            Wall(800, 0, 800, 600),
            Wall(0, 600, 800, 600)
        ]

    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.running = False

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        for r in self.rays:
            r.update(mouse_pos)
            for w in self.walls:
                r.cast(w)

    def draw(self, target_surf):
        target_surf.fill((0, 0, 0))
        for w in self.walls:
            w.draw(target_surf)
        for r in self.rays:
            r.draw(target_surf)
