import pygame as pg


class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = (200, 200, 200)

    def draw(self, target_surf):
        pg.draw.line(
            target_surf,
            self.color,
            (self.x1, self.y1),
            (self.x2, self.y2),
            3
        )