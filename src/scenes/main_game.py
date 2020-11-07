import pygame

from src.constants import *
from src.resources import controls, worlds
from src.scenes.scene import Scene, DevOverlay
from src import camera


class MainGame(Scene):
    def __init__(self, scene_manager, world_name):
        self.world = worlds[world_name]
        self.world_name = world_name
        self.world_map = self.world["map"]
        print(self.world_map.shape)
        super().__init__(scene_manager, MainGameDevOverlay)
        self.camera = camera.Camera(self.world)

    def update(self, dt):
        pass

    def draw(self):
        self.target_surface.fill((0, 64, 128))


class MainGameDevOverlay(DevOverlay):
    def __init__(self, scene):
        super().__init__(scene)
        self.world_name_surf, self.world_name_rect = self.font.render(
            f"world name: {self.scene.world_name}"
        )
        self.world_name_rect.topleft = self.fps_rect.bottomleft

    def draw(self):
        super().draw()
        self.target_surface.blit(self.world_name_surf, self.world_name_rect)
