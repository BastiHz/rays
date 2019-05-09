import math
import random
import pygame as pg
from ray import Ray
from wall import Wall


class TopView:
    def __init__(self, app):
        self.app = app
        self.color = (255, 196, 0)
        self.background_color = (20, 20, 20)
        self.ray_origin = (0, 0)
        self.rays = []
        for angle in range(0, 360, 5):
            self.rays.append(Ray(self.ray_origin, math.radians(angle)))
        w, h = self.app.main_surface.get_rect().size
        # -1 because otherwise w and h are off screen:
        w -= 1
        h -= 1
        self.walls = [
            # Wall(600, 200, 500, 500),
            Wall(0, 0, w, 0),
            Wall(0, 0, 0, h),
            Wall(w, 0, w, h),
            Wall(0, h, w, h)
        ]
        for _ in range(5):
            self.walls.append(Wall(
                random.randint(0, w),
                random.randint(0, h),
                random.randint(0, w),
                random.randint(0, h)
            ))

    def handle_input(self, event):
        pass

    def update(self):
        self.ray_origin = pg.mouse.get_pos()
        for r in self.rays:
            r.update_position(self.ray_origin)
            r.cast(self.walls)

    def draw(self, target_surf):
        target_surf.fill(self.background_color)
        # pg.draw.circle(target_surf, self.color, self.ray_origin, 3)
        for r in self.rays:
            r.draw(target_surf)
        for w in self.walls:
            w.draw(target_surf)
