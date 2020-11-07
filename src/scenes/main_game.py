import pygame

from src.constants import BACKGROUND_COLOR, SMALL_DISPLAY_WIDTH
from src.resources import controls, worlds
from src.scenes.scene import Scene, DevOverlay
from src import camera


class MainGame(Scene):
    def __init__(self, scene_manager, world_name):
        self.world = worlds[world_name]
        self.world_name = world_name
        super().__init__(scene_manager, MainGameDevOverlay)
        self.camera = camera.Camera(self.world)
        self.line_tops = []
        self.line_bottoms = []
        self.line_colors = []

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
        # elif event.type == pygame.ACTIVEEVENT:
        #     print(event.gain)

    def update(self, dt):
        self.line_tops, self.line_bottoms, self.line_colors = self.camera.cast_rays()

    def draw(self):
        self.target_surface.fill(BACKGROUND_COLOR)
        for x in range(SMALL_DISPLAY_WIDTH):
            pygame.draw.line(
                self.target_surface,
                self.line_colors[x],
                (x, self.line_tops[x]),
                (x, self.line_bottoms[x])
            )


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
