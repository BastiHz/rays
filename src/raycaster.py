import pygame
import numpy as np


from src.constants import *
from src.resources import options
from src import textures


np.seterr(divide='ignore')


def rgb_to_int(r, g, b):
    """Convert color tuples to ints.
    Normally I could call int() on a pygame.Color object but there
    seems to be a bug in the __int__() method of pygame.Color objects.
    Until that is fixed I do the conversion manually.

    r, g, and b must be integers

    I could also use a 3-dimensional np array and avoid the conversion
    to ints but blitting that to a surface seems to be slower than with
    a 2d array.
    """
    return (r << 16) + (g << 8) + b


def save_divide(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        return math.inf


class RayCaster:
    def __init__(self, world):
        self.position = pygame.Vector2(world["position_xy"])
        self.map_position_x = np.full(SMALL_DISPLAY_WIDTH, self.position.x, int)
        self.map_position_y = np.full(SMALL_DISPLAY_WIDTH, self.position.y, int)
        self.view_direction = pygame.Vector2(world["view_direction_xy"])
        camera_options = options["camera"]
        fov_radians = math.radians(camera_options["fov_degrees"])
        camera_plane_half_len = math.tan(fov_radians / 2)
        # View direction and camera plane must be perpendicular to each other.
        # So the camera plane is rotated 90 degrees counterclockwise to
        # the view direction.
        self.camera_plane = self.view_direction.rotate(90)
        self.camera_plane.scale_to_length(camera_plane_half_len)
        self.screen_height_half = SMALL_DISPLAY_HEIGHT // 2
        self.h = SMALL_DISPLAY_HEIGHT  # Change this to modify the perspective
        self.h_half = self.h / 2
        self.screen_bottom = SMALL_DISPLAY_HEIGHT - 1
        # camera_x is the x-coordinate on the camera plane which maps to
        # an x-coordinate on the screen. The left edge is -1 and the
        # right edge is +1.
        self.camera_x = np.linspace(-1, 1, SMALL_DISPLAY_WIDTH)
        self.world_map = world["map"]

        self.background_color = rgb_to_int(32, 32, 32)
        self.screen_buffer = np.full(
            SMALL_DISPLAY_SIZE,
            self.background_color
        )
        self.texture_width = 64
        self.texture_height = 64
        self.textures = textures.generate_textures(
            self.texture_width,
            self.texture_height
        )

        self.textures_dark = [tex >> 1 & 8355711 for tex in self.textures]
        # Insert a dummy at index 0 so the indices of the textures align with
        # their corresponding map integers. Because the lowest wall value is 1.
        self.textures.insert(0, None)
        self.textures_dark.insert(0, None)

        self.move_speed = camera_options["move_speed"]  # squares / s
        self.rotate_speed_keyboard = camera_options["rotate_speed_keyboard"]  # radians / s
        self.rotate_speed_mouse = camera_options["rotate_speed_mouse"] / SMALL_DISPLAY_WIDTH  # radians / pixel
        self.rotate_speed_mouse *= camera_options["rotate_speed_mouse_multiplier"]
        self.move_forward_velocity = self.view_direction * self.move_speed
        self.move_right_velocity = self.move_forward_velocity.rotate(90)

    def cast(self):
        # The vectorized version of this tutorial:
        # https://lodev.org/cgtutor/raycasting.html
        # My version looks a bit different from the tutorial and my map is
        # rotated by 90 degrees because of the way the map is stored. But
        # that doesn't matter.
        # And for some reason my textures are rotated or flipped.

        # Ideas for further improvements:
        # - Try pre-allocating the np arrays. For example np.divide()
        #   lets you specify an output array. Also overwrite instead of
        #   freshly allocate. Maybe I will have to make those into instance
        #   variables then.

        self.screen_buffer[...] = self.background_color

        ray_direction_x = self.view_direction.x + self.camera_plane.x * self.camera_x
        ray_direction_y = self.view_direction.y + self.camera_plane.y * self.camera_x

        # Delta distance could be calculated with pythagoras but only
        # the ratio between them is important which simplifies
        # the equation here.
        delta_distance_x = abs(np.divide(1, ray_direction_x))
        delta_distance_y = abs(np.divide(1, ray_direction_y))

        ray_dir_x_less_0 = ray_direction_x < 0
        step_x = np.where(ray_dir_x_less_0, -1, 1)
        side_distance_x = np.where(
            ray_dir_x_less_0,
            (self.position.x - self.map_position_x) * delta_distance_x,
            (self.map_position_x + 1 - self.position.x) * delta_distance_x
        )
        ray_dir_y_less_0 = ray_direction_y < 0
        step_y = np.where(ray_dir_y_less_0, -1, 1)
        side_distance_y = np.where(
            ray_dir_y_less_0,
            (self.position.y - self.map_position_y) * delta_distance_y,
            (self.map_position_y + 1 - self.position.y) * delta_distance_y
        )

        # perform DDA
        wall_x = self.map_position_x.copy()
        wall_y = self.map_position_y.copy()
        side = np.zeros(SMALL_DISPLAY_WIDTH, bool)  # Is it a north/south or west/east wall?
        wall_int = self.world_map[wall_y, wall_x]
        while any(i := wall_int == 0):
            x_lt_y = side_distance_x < side_distance_y
            i_and_x_lt_y = np.logical_and(i, x_lt_y)
            side_distance_x[i_and_x_lt_y] += delta_distance_x[i_and_x_lt_y]
            wall_x[i_and_x_lt_y] += step_x[i_and_x_lt_y]
            side[i_and_x_lt_y] = False
            i_and_y_ge_x = np.logical_and(i, np.logical_not(x_lt_y))
            side_distance_y[i_and_y_ge_x] += delta_distance_y[i_and_y_ge_x]
            wall_y[i_and_y_ge_x] += step_y[i_and_y_ge_x]
            side[i_and_y_ge_x] = True
            wall_int = self.world_map[wall_y, wall_x]

        # Calculate wall distance perpendicular to the camera plane.
        wall_distance = np.where(
            side,
            (wall_y - self.position.y + (1 - step_y) / 2) / ray_direction_y,
            (wall_x - self.position.x + (1 - step_x) / 2) / ray_direction_x
        )

        # Calculate length of vertical stripe.
        line_height = self.h // wall_distance
        line_height_half = line_height // 2
        line_top = np.maximum(self.screen_height_half - line_height_half, 0).astype(int)
        line_bottom = SMALL_DISPLAY_HEIGHT - line_top

        # Calculate where exactly the wall was hit.
        # The "% 1" has the ame effect as this line in
        # the tutorial: wallX -= floor((wallX))
        wall_x = np.where(
            side,
            (self.position.x + wall_distance * ray_direction_x) % 1,
            (self.position.y + wall_distance * ray_direction_y) % 1
        ) % 1

        # x coordinate on the texture
        tex_x = (wall_x * self.texture_width).astype(int)
        tex_x = np.where(
            np.logical_or(
                np.logical_and(np.logical_not(side), ray_direction_x > 0),
                np.logical_and(side, ray_direction_y < 0)
            ),
            self.texture_width - tex_x - 1,
            tex_x
        )

        # How much to increase the texture coordinate per screen pixel.
        step = self.texture_height / line_height
        # Starting texture coordinate.
        tex_pos_start = (line_top - self.h_half + line_height_half) * step
        for x in range(SMALL_DISPLAY_WIDTH):
            y = np.arange(line_top[x], line_bottom[x])
            tex_pos = tex_pos_start[x] + np.arange(len(y)) * step[x]
            # TODO: Maybe use "&" like in the tutorial instead of "%"?
            tex_y = (tex_pos % self.texture_height).astype(int)
            if side[x]:
                self.screen_buffer[x, y] = self.textures[wall_int[x]][tex_x[x], tex_y]
            else:
                self.screen_buffer[x, y] = self.textures_dark[wall_int[x]][tex_x[x], tex_y]

    def move_straight(self, sign, dt):
        # positive sign is forward, negative is backward
        self.move(self.position + self.move_forward_velocity * sign * dt)

    def move_sideways(self, sign, dt):
        # positive sign is right, negative is left
        self.move(self.position + self.move_right_velocity * sign * dt)

    def move(self, new_position):
        new_x_int = int(new_position.x)
        new_y_int = int(new_position.y)
        if self.world_map[new_y_int, new_x_int] == 0:
            self.position = new_position
            self.map_position_x[:] = new_x_int
            self.map_position_y[:] = new_y_int

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
