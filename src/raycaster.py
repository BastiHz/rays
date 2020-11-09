import pygame
import numpy


from src.constants import *
from src.resources import options


class RayCaster:
    def __init__(self, world):
        self.position = pygame.Vector2(world["position_xy"])
        self.view_direction = pygame.Vector2(world["view_direction_xy"])
        camera_options = options["camera"]
        fov_radians = math.radians(camera_options["fov_degrees"])
        camera_plane_half_len = math.tan(fov_radians / 2)
        # View direction and camera plane must be perpendicular to each other.
        # So the camera plane is rotated 90 degrees counterclockwise to
        # the view direction.
        self.camera_plane = self.view_direction.rotate(90)
        self.camera_plane.scale_to_length(camera_plane_half_len)

        self.screen_height_half = SMALL_DISPLAY_HEIGHT / 2
        self.screen_bottom = SMALL_DISPLAY_HEIGHT - 1
        # camera_x is the x-coordinate on the camera plane which maps to
        # an x-coordinate on the screen. The left edge is -1 and the
        # right edge is +1.
        self.camera_x = numpy.linspace(-1, 1, SMALL_DISPLAY_WIDTH)
        self.world_map = world["map"]
        self.colors = world["colors"]
        self.dark_colors = [[c // 2 for c in color] for color in self.colors]
        self.move_speed = camera_options["move_speed"]  # squares / s
        self.rotate_speed_keyboard = camera_options["rotate_speed_keyboard"]  # radians / s
        self.rotate_speed_mouse = camera_options["rotate_speed_mouse"]  # radians / pixel
        self.rotate_speed_mouse *= camera_options["rotate_speed_mouse_multiplier"]
        self.move_forward_velocity = self.view_direction * self.move_speed
        self.move_right_velocity = self.move_forward_velocity.rotate(90)

    def cast(self):
        # # https://lodev.org/cgtutor/raycasting.html
        # This function needs to be fast, so there is minimal use of
        # Vector2 here.
        map_position_x = int(self.position.x)
        map_position_y = int(self.position.y)
        line_tops = []
        line_bottoms = []
        line_colors = []
        for camera_x in self.camera_x:
            ray_direction_x, ray_direction_y = self.view_direction + self.camera_plane * camera_x

            # Delta distance could be calculated with pythagoras but only
            # the ratio between them is important, so this simplifies
            # the equation here.
            delta_distance_x = abs(save_divide(1, ray_direction_x))
            delta_distance_y = abs(save_divide(1, ray_direction_y))

            if ray_direction_x < 0:
                step_x = -1
                side_distance_x = (self.position.x - map_position_x) * delta_distance_x
            else:
                step_x = 1
                side_distance_x = (map_position_x + 1 - self.position.x) * delta_distance_x
            if ray_direction_y < 0:
                step_y = -1
                side_distance_y = (self.position.y - map_position_y) * delta_distance_y
            else:
                step_y = 1
                side_distance_y = (map_position_y + 1 - self.position.y) * delta_distance_y

            wall_x = map_position_x
            wall_y = map_position_y
            side = None
            while (wall_int := self.world_map[wall_y, wall_x]) == 0:
                # jump to next map square, OR in x-direction, OR in y-direction
                if side_distance_x < side_distance_y:
                    side_distance_x += delta_distance_x
                    wall_x += step_x
                    side = 0
                else:
                    side_distance_y += delta_distance_y
                    wall_y += step_y
                    side = 1

            # Calculate wall distance perpendicular to the camera plane.
            if side == 0:
                wall_distance = (wall_x - self.position.x + (1 - step_x) / 2) / ray_direction_x
            else:
                wall_distance = (wall_y - self.position.y + (1 - step_y) / 2) / ray_direction_y

            line_height_half = self.screen_height_half / wall_distance
            line_tops.append(max(self.screen_height_half - line_height_half, 0))
            line_bottoms.append(min(
                self.screen_height_half + line_height_half,
                self.screen_bottom
            ))

            if side == 0:
                line_colors.append(self.colors[wall_int])
            else:
                line_colors.append(self.dark_colors[wall_int])

        return line_tops, line_bottoms, line_colors

    def move_straight(self, sign, dt):
        # positive sign is forward, negative is backward
        new_x, new_y = self.position + self.move_forward_velocity * sign * dt
        if self.world_map[int(new_y), int(new_x)] == 0:
            self.position.update(new_x, new_y)

    def move_sideways(self, sign, dt):
        # positive sign is right, negative is left
        new_x, new_y = self.position + self.move_right_velocity * sign * dt
        if self.world_map[int(new_y), int(new_x)] == 0:
            self.position.update(new_x, new_y)

    def rotate_keyboard(self, sign, dt):
        # positive sign is right, negative is left
        # This is because rotation happens in normal coordinates where y
        # increases upwards, not in screen coordinates where it increases
        # downwards.
        self.rotate(self.rotate_speed_keyboard * dt * sign)

    def rotate_mouse(self, mouse_rel_x):
        self.rotate(self.rotate_speed_mouse * mouse_rel_x)

    def rotate(self, angle):
        self.view_direction.rotate_ip_rad(angle)
        self.camera_plane.rotate_ip_rad(angle)
        self.move_forward_velocity.rotate_ip_rad(angle)
        self.move_right_velocity.rotate_ip_rad(angle)


def save_divide(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        return math.inf
