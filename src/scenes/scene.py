import pygame

from src.constants import *
from src.resources import controls, fonts


def scale_mouse(pos_or_rel):
    """Adjust the mouse position or relative motion from screen coordinates
    to small display coordinates.
    """
    return (
        pos_or_rel[0] / DISPLAY_MAGNIFICATION,
        pos_or_rel[1] / DISPLAY_MAGNIFICATION
    )


class Scene:
    def __init__(self, scene_manager, dev_overlay):
        self.scene_manager = scene_manager
        self.target_surface = scene_manager.small_display
        if dev_overlay is None:
            self.dev_overlay = DevOverlay(self)
        else:
            self.dev_overlay = dev_overlay(self)
        self.is_done = False
        self.mouse_position = (0, 0)

    def start(self):
        self.is_done = False

    def close(self, next_scene_name=""):
        """Quit or suspend a scene. Use this for cleanup."""
        self.is_done = True
        self.scene_manager.persistent_scene_data["next scene name"] = next_scene_name

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.close()
        if (event.type == pygame.KEYDOWN and
                event.key == controls[TOGGLE_DEV_OVERLAY]):
            self.scene_manager.dev_overlay_visible = \
                not self.scene_manager.dev_overlay_visible
        elif event.type == pygame.MOUSEMOTION:
            event.pos = scale_mouse(event.pos)
            event.rel = scale_mouse(event.rel)
            self.mouse_position = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event.pos = scale_mouse(event.pos)
            self.mouse_position = event.pos

    def update(self, dt):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError


class DevOverlay:
    def __init__(self, scene):
        self.scene = scene
        self.scene_manager = scene.scene_manager
        self.target_surface = self.scene_manager.main_display
        self.font = fonts["dev_font"]
        self.text_margin = pygame.Vector2(5, 5)
        self.fps = -1
        self.fps_surf, self.fps_rect = self.font.render(f"FPS: {self.fps}")
        self.fps_rect.topleft = self.text_margin

    def update(self):
        fps = int(self.scene_manager.clock.get_fps())
        if fps != self.fps:
            self.fps = fps
            self.fps_surf, self.fps_rect = self.font.render(f"FPS: {fps}")
            self.fps_rect.topleft = self.text_margin

    def draw(self):
        self.target_surface.blit(self.fps_surf, self.fps_rect)
