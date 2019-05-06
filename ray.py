import math
import pygame as pg


class Ray:
    def __init__(self, pos, angle):
        self.x1, self.y1 = pos
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)
        self.x2 = self.x1 + self.dx
        self.y2 = self.y1 + self.dy
        self.color = (255, 128, 0)
        self.wall_intersect = []

    def update(self, pos):
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
            pg.draw.circle(
                target_surf,
                self.color,
                (int(self.wall_intersect[0]),
                 int(self.wall_intersect[1])),
                5
            )
        else:
            pg.draw.line(
                target_surf,
                self.color,
                (self.x1, self.y1),
                (self.x2, self.y2)
            )

    def cast(self, wall):
        self.wall_intersect = ()
        denominator = ((wall.x1 - wall.x2) * (self.y1 - self.y2)
                       - (wall.y1 - wall.y2) * (self.x1 - self.x2))
        if denominator == 0:
            return
        t = (((wall.x1 - self.x1) * (self.y1 - self.y2)
              - (wall.y1 - self.y1) * (self.x1 - self.x2)) / denominator)
        u = -((wall.x1 - wall.x2) * (wall.y1 - self.y1)
              - (wall.y1 - wall.y2) * (wall.x1 - self.x1)) / denominator
        if 0 < t < 1 and u > 0:
            self.wall_intersect = (
                    wall.x1 + t * (wall.x2 - wall.x1),
                    wall.y1 + t * (wall.y2 - wall.y1)
            )

        # FIXME: Determine closes wall, not last tested. Use only closest for self.wall_intersect.
