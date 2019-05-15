import math
import numpy
import pygame as pg


class RayCaster:
    def __init__(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading
        self.move_speed = 40  # px/s
        self.turn_speed = math.pi / 2  # rad/s
        self.rays = []
        self.hits = []  # stores the distances to the walls or None if a ray didn't hit a wall

    def make_new_rays(self, fov, n):
        self.rays = []
        for angle in numpy.linspace(-fov / 2, fov / 2, n):
            self.rays.append(Ray(self.x, self.y, self.heading, angle))
        self.hits = [None] * len(self.rays)

    def handle_input(self, events, pressed, dt):
        if pressed[pg.K_w]:
            self.move(dt, 1)
        if pressed[pg.K_s]:
            self.move(dt, -1)
        if pressed[pg.K_d]:
            self.turn(dt, 1)
        if pressed[pg.K_a]:
            self.turn(dt, -1)

    def move(self, sign, dt):
        # positive sign means forward, negative backward
        dx = math.cos(self.heading) * self.move_speed * dt * sign
        dy = math.sin(self.heading) * self.move_speed * dt * sign
        for r in self.rays:
            r.move(dx, dy)

    def turn(self, sign, dt):
        # positive sign means right, negative means left
        self.heading += self.turn_speed * dt * sign
        for r in self.rays:
            r.rotate(self.heading)

    def update(self, dt, walls):
        for i, r in enumerate(self.rays):
            self.hits[i] = r.cast(walls)

    def draw(self, target_surface):
        for r in self.rays:
            r.draw(target_surface)


class Ray:
    def __init__(self, x, y, heading, relative_angle):
        self.x1 = x
        self.y1 = y
        # relative_angle is the angle relative to the raycasters heading
        self.relative_angle = relative_angle
        angle = relative_angle + heading
        self.x2 = self.x1 + math.cos(angle)
        self.y2 = self.y1 + math.sin(angle)
        self.color = (255, 196, 0)
        self.wall_intersect = []

    def move(self, dist_x, dist_y):
        self.x1 += dist_x
        self.y1 += dist_y
        self.x2 += dist_x
        self.y2 += dist_y
        
    def rotate(self, new_heading):
        angle = new_heading + self.relative_angle
        self.x2 = self.x1 + math.cos(angle)
        self.y2 = self.y1 + math.sin(angle)

    def draw(self, target_surf):
        if self.wall_intersect:
            pg.draw.line(
                target_surf,
                self.color,
                (self.x1, self.y1),
                self.wall_intersect
            )

    def cast(self, walls):
        # Algorithm taken from https://www.youtube.com/watch?v=-6iIc6-Y-kk
        # which references https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
        # I check t with 0 <= t <= 1 like it says in wikipedia,
        # however thecodingtrain only uses '<' in the video.
        # I don't believe it matters much.
        self.wall_intersect = ()
        min_distance = math.inf
        for w in walls:
            denominator = ((w.x1 - w.x2) * (self.y1 - self.y2)
                           - (w.y1 - w.y2) * (self.x1 - self.x2))
            if denominator == 0:
                continue
            t = (((w.x1 - self.x1) * (self.y1 - self.y2)
                  - (w.y1 - self.y1) * (self.x1 - self.x2)) / denominator)
            u = -((w.x1 - w.x2) * (w.y1 - self.y1)
                  - (w.y1 - w.y2) * (w.x1 - self.x1)) / denominator
            if 0 <= t <= 1 and u > 0:
                intersect_x = w.x1 + t * (w.x2 - w.x1)
                intersect_y = w.y1 + t * (w.y2 - w.y1)
                if u < min_distance:
                    min_distance = u
                    self.wall_intersect = (intersect_x, intersect_y)

        # TODO: return the distance u if a wall is hit or otherwise none.