from typing import TYPE_CHECKING

import pygame

from src.constants import *
from src.resources import controls
from src.scenes.scene import Scene, DevOverlay


if TYPE_CHECKING:
    from src.game import Game


class MainGame(Scene):
    def __init__(self, scene_manager: "Game") -> None:
        super().__init__(scene_manager, MainGameDevOverlay)

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        self.target_surface.fill((0, 64, 128))


class MainGameDevOverlay(DevOverlay):
    def __init__(self, scene: MainGame,) -> None:
        super().__init__(scene)
