import pygame as pg


class TopView:
    def __init__(self, app):
        self.app = app

    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.running = False

    def update(self):
        pass

    def draw(self, target_surf):
        pass
