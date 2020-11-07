import math

import pygame
import numpy


from src.constants import FOV, SMALL_DISPLAY_WIDTH


class Camera:
    def __init__(self, world):
        self.position = pygame.Vector2(world["position_xy"])
        self.view_direction = pygame.Vector2(world["view_direction_xy"])
        self.camera_plane = pygame.Vector2(0, math.tan(math.radians(FOV / 2)))
        # View direction and camera plane must be perpendicular to each other.
        assert round(self.camera_plane.angle_to(self.view_direction)) == 90
        self.n_rays = SMALL_DISPLAY_WIDTH
        self.camera_x = numpy.linspace(-1, 1, self.n_rays)

    def cast(self):
        # This function needs to be fast, so there is minimal use of
        # Vector2 here.
        for cx in self.camera_x:
            ray_direction_x, ray_direction_y = self.view_direction + self.camera_plane * cx
            # FIXME: Isn't this backwards? I think this will go right to left
            #  instead of left to right. First implement the rest and see how
            #  it goes.

