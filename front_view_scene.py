import pygame as pg


class FrontView:
    def __init__(self, x, y, w, h, raycaster):
        self.raycaster = raycaster
        self.rect = pg.Rect(x, y, w, h)
        self.surface = pg.Surface((w, h))
        self.background_color = (20, 20, 20)

    def update(self, dt):
        pass

    def handle_input(self, events, pressed, dt):
        pass

    def draw(self, target_surface):
        self.surface.fill(self.background_color)

        # TODO: handle distance, wall brightness, wall size (line height) and distortion

        target_surface.blit(self.surface, self.rect)
