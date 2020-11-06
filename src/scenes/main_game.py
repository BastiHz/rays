import pygame

from src.constants import *
from src.resources import controls
from src.scenes.scene import Scene, DevOverlay


class MainGame(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager, MainGameDevOverlay)

    def update(self, dt):
        pass

    def draw(self):
        self.target_surface.fill((0, 64, 128))


class MainGameDevOverlay(DevOverlay):
    def __init__(self, scene):
        super().__init__(scene)
