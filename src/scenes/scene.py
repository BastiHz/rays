from typing import Optional, TYPE_CHECKING

import pygame

from src.constants import *
from src.resources import controls


if TYPE_CHECKING:
    from src.game import Game


class Scene:
    def __init__(
        self,
        scene_manager: "Game",
        dev_overlay: "DevOverlay" = None
    ) -> None:
        self.scene_manager = scene_manager
        self.target_surface = scene_manager.small_display
        if dev_overlay is None:
            self.dev_overlay = DevOverlay(self)
        else:
            self.dev_overlay = dev_overlay(self)
        self.is_done = False

    def start(self) -> None:
        self.is_done = False

    def close(self, next_scene_name: str = "") -> None:
        """Quit or suspend a scene. Use this for cleanup."""
        self.is_done = True
        self.scene_manager.persistent_scene_data["next scene name"] = next_scene_name

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.close()
        elif event.type == pygame.KEYDOWN:
            if event.key == controls[TOGGLE_DEV_OVERLAY]:
                self.scene_manager.dev_overlay_visible = \
                    not self.scene_manager.dev_overlay_visible

    def update(self, dt: float) -> None:
        raise NotImplementedError

    def draw(self) -> None:
        raise NotImplementedError


class DevOverlay:
    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        self.scene_manager = scene.scene_manager
        self.target_surface = self.scene_manager.main_display
        # self.dev_font = pygame.freetype.Font(DEV_FONT_PATH, DEV_FONT_SIZE)
        # self.dev_font.pad = True
        # self.dev_font.fgcolor = DEV_COLOR
        # self.dev_margin = pygame.Vector2(10, 10)
        #
        # self.fps_text = ""
        # self.fps_surf = None
        # self.fps_rect = None

    def update(self) -> None:
        fps = int(self.scene_manager.clock.get_fps())
        # if new_fps_text != self.fps_text:
        #     self.fps_text = new_fps_text
        #     self.fps_text, self.fps_rect = self.dev_font.render(self.fps_text)
        #     self.fps_rect.topleft = self.dev_margin

    def draw(self) -> None:
        pass
        # self.target_surface.blit(self.fps_text, self.fps_rect)
