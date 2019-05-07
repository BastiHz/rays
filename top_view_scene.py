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
        self.walls = [
            # Wall(600, 200, 500, 500),
            Wall(0, 0, 800, 0),
            Wall(0, 0, 0, 600),
            Wall(800-2, 0, 800-2, 600),  # 2 = hardcoded wall thickness
            Wall(0, 600-2, 800, 600-2)   # '-2' makes left and lower wall visible
        ]
        w, h = self.app.main_surface.get_rect().size
        for _ in range(5):
            self.walls.append(Wall(
                random.randint(0, w),
                random.randint(0, h),
                random.randint(0, w),
                random.randint(0, h)
            ))

    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.running = False

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
