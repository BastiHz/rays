import pygame
import numpy as np


from src.constants import *
from src.resources import options
from src import textures


np.seterr(divide='ignore')


class RayCaster:
    def __init__(self, world):
        x, y = pygame.Vector2(world["position xy"])
        if x % 1 != 0 or y % 1 != 0:
            raise ValueError("\"position_xy\" must be a tuple of integers.")
        # Add 0.5 so that the camera starts in the middle of a cell.
        self.position = pygame.Vector2(x + 0.5, y + 0.5)
        self.map_position_x = np.full(SMALL_DISPLAY_WIDTH, self.position.x, int)
        self.map_position_y = np.full(SMALL_DISPLAY_WIDTH, self.position.y, int)
        self.view_direction = pygame.Vector2(world["view direction xy"])
        self.view_direction.scale_to_length(1)
        camera_options = options["camera"]
        fov_radians = math.radians(camera_options["fov degrees"])
        camera_plane_half_len = math.tan(fov_radians / 2)
        # View direction and camera plane must be perpendicular to each other.
        # So the camera plane is rotated 90 degrees counterclockwise to
        # the view direction.
        self.camera_plane = self.view_direction.rotate(90)
        self.camera_plane.scale_to_length(camera_plane_half_len)
        self.screen_height_half = SMALL_DISPLAY_HEIGHT // 2
        # h and h_half can be changed to modify the perspective. But with an
        # aspect ratio of 4:3 and an fov of 66° it works nicely when
        # h is the display height. Never tried to change it, though.
        self.h = SMALL_DISPLAY_HEIGHT
        self.h_half = self.h / 2
        self.screen_bottom = SMALL_DISPLAY_HEIGHT - 1
        # camera_x is the x-coordinate on the camera plane which maps to
        # an x-coordinate on the screen. The left edge is -1 and the
        # right edge is +1.
        self.camera_x = np.linspace(-1, 1, SMALL_DISPLAY_WIDTH)
        self.world_map = world["map"]
        if self.world_map[self.map_position_y[0], self.map_position_x[0]] != 0:
            raise ValueError("Start position is inside wall.")
        self.screen_x = np.arange(SMALL_DISPLAY_WIDTH)
        self.screen_y = np.arange(SMALL_DISPLAY_HEIGHT)
        self.ceiling_y = np.arange(self.screen_height_half)
        self.floor_y = SMALL_DISPLAY_HEIGHT - 1 - self.ceiling_y
        # Vertical position of the camera. Exactly in the middle, so that half
        # the screen is below and half is above. That's why
        # SMALL_DISPLAY_HEIGHT must be an even number or else the center row
        # would be neither floor nor ceiling.
        camera_y = (SMALL_DISPLAY_HEIGHT - 1) / 2
        # Horizontal distance from the viewer to the ceiling rows.
        self.row_distance = camera_y / (camera_y - self.ceiling_y)
        # Ray direction for leftmost and rightmos ray.
        self.ray_direction_left = self.view_direction - self.camera_plane
        self.ray_direction_right = self.view_direction + self.camera_plane
        self.ceiling_pixels = None
        self.floor_pixels = None
        self.walls_screen_y = [None] * SMALL_DISPLAY_WIDTH
        self.wall_pixels = [None] * SMALL_DISPLAY_WIDTH

        self.texture_width = 64
        self.texture_height = 64
        self.textures = textures.generate_walls(
            self.texture_width,
            self.texture_height
        )
        self.textures_dark = [tex >> 1 & 8355711 for tex in self.textures]
        # Insert a dummy at index 0 so the indices of the textures align with
        # their corresponding map integers. Because the lowest wall value is 1.
        self.textures.insert(0, None)
        self.textures_dark.insert(0, None)
        self.floor_texture = textures.generate_floor(
            self.texture_width,
            self.texture_height
        )
        self.ceiling_texture = textures.generate_ceiling(
            self.texture_width,
            self.texture_height
        )

        self.move_speed = camera_options["move speed"]  # squares / s
        self.rotate_speed_keyboard = camera_options["rotate speed keyboard"]  # radians / s
        self.rotate_speed_mouse = camera_options["rotate speed mouse"] / SMALL_DISPLAY_WIDTH  # radians / pixel
        self.rotate_speed_mouse *= camera_options["rotate speed mouse multiplier"]
        self.move_forward_velocity = self.view_direction * self.move_speed
        self.move_right_velocity = self.move_forward_velocity.rotate(90)

        self.refresh_rays = True

    def cast(self):
        if self.refresh_rays:
            self.cast_floor_ceiling()
            self.cast_walls()
            self.refresh_rays = False

    def cast_floor_ceiling(self):
        # Only self.ceiling is used in most of the calculations because floor
        # and ceiling are symmetrical.

        # to calculate the real world step vector we have to add for each x
        # (parallel to camera plane)
        step_x = np.outer(
            self.screen_x,
            self.row_distance
            * (self.ray_direction_right.x - self.ray_direction_left.x)
            / SMALL_DISPLAY_WIDTH
        )
        step_y = np.outer(
            self.screen_x,
            self.row_distance
            * (self.ray_direction_right.y - self.ray_direction_left.y)
            / SMALL_DISPLAY_WIDTH
        )

        # world coordinates of floor and ceiling hits
        ray_pos_x = step_x + np.broadcast_to(
            self.position.x + self.row_distance * self.ray_direction_left.x,
            (SMALL_DISPLAY_WIDTH, self.screen_height_half)
        )
        ray_pos_y = step_y + np.broadcast_to(
            self.position.y + self.row_distance * self.ray_direction_left.y,
            (SMALL_DISPLAY_WIDTH, self.screen_height_half)
        )

        # get the texture coordinate from the fractional part
        # The "% 1" gets the fractional part.
        # TODO: Do I really need to protect against negative coordinates?
        #   In the tex_y_floor line I could also turn the subtraction around
        #   and use negative coordinates.
        tex_x = (self.texture_width * (ray_pos_x % 1)).astype(int)
        tex_y_ceiling = (self.texture_height * (ray_pos_y % 1)).astype(int)
        tex_y_floor = self.texture_height - 1 - tex_y_ceiling
        self.ceiling_pixels = self.ceiling_texture[tex_x, tex_y_ceiling]
        self.floor_pixels = self.floor_texture[tex_x, tex_y_floor]

    def cast_walls(self):
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
            wall_int[...] = self.world_map[wall_y, wall_x]

        # Calculate wall distance perpendicular to the camera plane.
        wall_distance = np.where(
            side,
            (wall_y - self.position.y + (1 - step_y) / 2) / ray_direction_y,
            (wall_x - self.position.x + (1 - step_x) / 2) / ray_direction_x
        )

        # Calculate length of vertical stripe.
        line_height = self.h / wall_distance
        line_height_half = line_height / 2
        line_top = np.maximum(self.screen_height_half - line_height_half, 0)
        line_bottom = SMALL_DISPLAY_HEIGHT - line_top

        # Calculate where exactly the wall was hit to get
        # the x-coordinate on the texture.
        # The "% 1" gets the fractional part.
        tex_x = np.where(
            side,
            self.position.x + wall_distance * ray_direction_x,
            self.position.y + wall_distance * ray_direction_y
        )
        tex_x = ((tex_x % 1) * self.texture_width).astype(int)

        # TODO: Find out what effect this step has and if I can remove it.
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

        for x in self.screen_x:
            y = np.arange(line_top[x], line_bottom[x], dtype=int)
            self.walls_screen_y[x] = y
            tex_y = (tex_pos_start[x] + np.arange(len(y)) * step[x]).astype(int)
            if side[x]:
                self.wall_pixels[x] = self.textures[wall_int[x]][tex_x[x], tex_y]
            else:
                self.wall_pixels[x] = self.textures_dark[wall_int[x]][tex_x[x], tex_y]

    def draw(self, target_surface):
        # Using pygame.surfarray.pixels2d() with a temporary screen buffer is
        # faster than using pygame.surfarray.blit_array(). The screen buffer
        # here has to be temporary because during its lifetime the surface is
        # locked and cannot be blitted to or from.
        screen_buffer = pygame.surfarray.pixels2d(target_surface)
        # ceiling and floor:
        screen_buffer[:, self.ceiling_y] = self.ceiling_pixels
        screen_buffer[:, self.floor_y] = self.floor_pixels
        # walls:
        # TODO: Can it be done without the loop?
        for x in self.screen_x:
            screen_buffer[x, self.walls_screen_y[x]] = self.wall_pixels[x]

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
            self.map_position_x[...] = new_x_int
            self.map_position_y[...] = new_y_int
            self.refresh_rays = True

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
        self.refresh_rays = True
        self.ray_direction_left.rotate_ip_rad(angle)
        self.ray_direction_right.rotate_ip_rad(angle)
