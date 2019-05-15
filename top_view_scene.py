import pygame as pg
from wall import Wall


class TopView:
    def __init__(self, x, y, w, h, raycaster):
        self.raycaster = raycaster
        self.rect = pg.Rect(x, y, w, h)
        self.surface = pg.Surface((w, h))
        self.background_color = (20, 20, 20)

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

    def handle_input(self, events, pressed, dt):
        pass

    def update(self, dt):
        self.raycaster.update(dt, self.walls)
        # FIXME: Walls should not be a property of this scene. Maybe store them in main?

    def draw(self, target_surface):
        self.surface.fill(self.background_color)
        self.raycaster.draw(self.surface)
        for w in self.walls:
            w.draw(self.surface)
        target_surface.blit(self.surface, self.rect)
