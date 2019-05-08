import math
import pygame as pg


class Ray:
    def __init__(self, pos, angle):
        self.x1, self.y1 = pos
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)
        self.x2 = self.x1 + self.dx
        self.y2 = self.y1 + self.dy
        self.color = (255, 196, 0)
        self.wall_intersect = []

    def update_position(self, pos):
        self.x1, self.y1 = pos
        self.x2 = self.x1 + self.dx
        self.y2 = self.y1 + self.dy

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
