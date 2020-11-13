import pygame
import numpy as np


from src.constants import *
from src.resources import options
from src import textures


np.seterr(divide='ignore')


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

        self.screen_buffer = np.zeros(SMALL_DISPLAY_SIZE, int)
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
        self.floor_texture = self.textures[2]
        self.ceiling_texture = self.textures[3]

        self.move_speed = camera_options["move_speed"]  # squares / s
        self.rotate_speed_keyboard = camera_options["rotate_speed_keyboard"]  # radians / s
        self.rotate_speed_mouse = camera_options["rotate_speed_mouse"] / SMALL_DISPLAY_WIDTH  # radians / pixel
        self.rotate_speed_mouse *= camera_options["rotate_speed_mouse_multiplier"]
        self.move_forward_velocity = self.view_direction * self.move_speed
        self.move_right_velocity = self.move_forward_velocity.rotate(90)

    def cast(self):
        self.cast_floor_ceiling()
        self.cast_walls()

    def cast_floor_ceiling(self):
        # https://lodev.org/cgtutor/raycasting2.html

        # TODO: vectorize this
        for y in range(SMALL_DISPLAY_HEIGHT):
            # rayDir for leftmost ray (x = 0) and rightmost ray (x = w)
            ray_dir_x_0 = self.view_direction.x - self.camera_plane.x
            ray_dir_y_0 = self.view_direction.y - self.camera_plane.y
            ray_dir_x_1 = self.view_direction.x + self.camera_plane.x
            ray_dir_y_1 = self.view_direction.y + self.camera_plane.y

            # Current y position compared to the center of the screen (the horizon)
            p = y - self.screen_height_half
            if p == 0:
                # Why isn't this handled in the tutorial?
                # However it shouldn't matter because there will always be
                # walls at the horizon.
                continue

            # Vertical position of the camera.
            pos_z = self.screen_height_half  # FIXME: unnecessary, remove this

            # Horizontal distance from the camera to the floor for the current row.
            # 0.5 is the z position exactly in the middle between floor and ceiling.
            row_distance = pos_z / p

            # calculate the real world step vector we have to add for each x 
            # (parallel to camera plane), adding step by step avoids 
            # multiplications with a weight in the inner loop
            floor_step_x = row_distance * (ray_dir_x_1 - ray_dir_x_0) / SMALL_DISPLAY_WIDTH
            floor_step_y = row_distance * (ray_dir_y_1 - ray_dir_y_0) / SMALL_DISPLAY_WIDTH
            
            # real world coordinates of the leftmost column. This will be 
            # updated as we step to the right.
            floor_x = self.position.x + row_distance * ray_dir_x_0
            floor_y = self.position.y + row_distance * ray_dir_y_0

            for x in range(SMALL_DISPLAY_WIDTH):
                # the cell coord is simply got from the integer parts 
                # of floor_x and floor_y
                cell_x = int(floor_x)
                cell_y = int(floor_y)
            
                # get the texture coordinate from the fractional part
                tex_x = int(self.texture_width * (floor_x - cell_x)) % self.texture_width
                tex_y = int(self.texture_height * (floor_y - cell_y)) % self.texture_height

                floor_x += floor_step_x
                floor_y += floor_step_y

                # floor
                self.screen_buffer[x, y] = self.floor_texture[tex_x, tex_y]
                # ceiling (symmetrical, at SMALL_DISPLAY_HEIGHT - y - 1 instead of y)
                self.screen_buffer[x, SMALL_DISPLAY_HEIGHT - y - 1] = self.ceiling_texture[tex_x, tex_y]

    def cast_walls(self):
        # The vectorized version of this tutorial:
        # https://lodev.org/cgtutor/raycasting.html

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
        # The "% 1" has the same effect as this line in
        # the tutorial: wallX -= floor((wallX))
        tex_x = ((np.where(
            side,
            (self.position.x + wall_distance * ray_direction_x),
            (self.position.y + wall_distance * ray_direction_y)
        ) % 1) * self.texture_width).astype(int)
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
            y = np.arange(line_top[x], line_bottom[x], dtype=int)
            tex_y = (tex_pos_start[x] + np.arange(len(y)) * step[x]).astype(int)
            # The tutorial has this additional step here :
            # int texY = (int)texPos & (texHeight - 1);
            # Which I wrote as:
            # tex_y = tex_y % self.texture_height
            # But this seems unnecessary because why would tex_pos ever be
            # greater than texture_height? So I removed it which makes the loop
            # significantly faster.
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
            self.map_position_x[...] = new_x_int
            self.map_position_y[...] = new_y_int

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
