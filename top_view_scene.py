import math
import numpy
import pygame as pg
from ray import Ray
from wall import Wall


class TopView:
    def __init__(self, w, h):
        self.color = (255, 196, 0)
        self.background_color = (20, 20, 20)
        self.rect = pg.Rect(0, 0, w, h)
        self.surface = pg.Surface((w, h))
        self.ray_origin = [w // 2, h // 2]
        self.view_direction = 0
        self.move_speed = 30  # px/s
        self.turn_speed = math.radians(50)  # rad/s
        self.fov = math.radians(90)  # field of view
        self.rays = []
        for angle in numpy.linspace(-self.fov / 2, self.fov / 2, w):
            self.rays.append(Ray(self.ray_origin, angle))
        # -1 because otherwise w and h are off screen:
        w -= 1
        h -= 1
        self.walls = [
            Wall(0, 0, w, 0),  # top
            Wall(0, 0, 0, h),  # left
            Wall(w, 0, w, h),  # right
            Wall(0, h, w, h),  # bottom
            # cube:
            Wall(100, 75, 100, 150),
            Wall(100, 150, 175, 150),
            Wall(175, 150, 175, 75),
            Wall(175, 75, 100, 75),
            # triangle:
            Wall(200, 250, 250, 350),
            Wall(250, 350, 150, 350),
            Wall(150, 350, 200, 250),
            # spiral:
            Wall(300, 50, 375, 50),
            Wall(375, 50, 375, 190),
            Wall(300, 50, 300, 125),
            Wall(300, 125, 340, 125),
            Wall(340, 125, 340, 80),
            Wall(375, 190, 300, 190)
        ]
        
    def move_forward(self, dt):
        dx = math.cos(self.view_direction) * self.move_speed * dt
        dy = math.sin(self.view_direction) * self.move_speed * dt
        for r in self.rays:
            r.move(dx, dy)
            
    def move_backward(self, dt):
        dx = math.cos(self.view_direction) * -self.move_speed * dt
        dy = math.sin(self.view_direction) * -self.move_speed * dt
        for r in self.rays:
            r.move(dx, dy)
    
    def turn_left(self, dt):
        turn_angle = -self.turn_speed * dt
        self.view_direction += turn_angle
        for r in self.rays:
            r.rotate(turn_angle)
        
    def turn_right(self, dt):
        turn_angle = self.turn_speed * dt
        self.view_direction += turn_angle
        for r in self.rays:
            r.rotate(turn_angle)

    def update(self, events, pressed, dt):
        if pressed[pg.K_w]:
            self.move_forward(dt)
        if pressed[pg.K_s]:
            self.move_backward(dt)
        if pressed[pg.K_a]:
            self.turn_left(dt)
        if pressed[pg.K_d]:
            self.turn_right(dt)
        for r in self.rays:
            r.cast(self.walls)

    def draw(self, target_surf):
        self.surface.fill(self.background_color)
        for r in self.rays:
            r.draw(self.surface)
        for w in self.walls:
            w.draw(self.surface)
        target_surf.blit(self.surface, self.rect)
