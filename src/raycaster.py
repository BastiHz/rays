import pygame
import numpy


from src.constants import *
from src.resources import options
from src import textures


def rgb_to_int(r, g, b):
    """Convert color tuples to ints.
    Normally I could call int() on a pygame.Color object but there
    seems to be a bug in the __int__() method of pygame.Color objects.
    Until that is fixed I do the conversion manually.

    r, g, and b must be integers

    I could also use a 3-dimensional numpy array and avoid the conversion
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
        self.map_position_x = int(self.position.x)
        self.map_position_y = int(self.position.y)
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
        self.screen_bottom = SMALL_DISPLAY_HEIGHT - 1
        # camera_x is the x-coordinate on the camera plane which maps to
        # an x-coordinate on the screen. The left edge is -1 and the
        # right edge is +1.
        self.camera_x = numpy.linspace(-1, 1, SMALL_DISPLAY_WIDTH)
        self.world_map = world["map"]

        self.background_color = rgb_to_int(32, 32, 32)
        self.screen_buffer = numpy.full(
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
        self.rotate_speed_mouse = camera_options["rotate_speed_mouse"]  # radians / pixel
        self.rotate_speed_mouse *= camera_options["rotate_speed_mouse_multiplier"]
        self.move_forward_velocity = self.view_direction * self.move_speed
        self.move_right_velocity = self.move_forward_velocity.rotate(90)

    def cast(self):
        # https://lodev.org/cgtutor/raycasting.html
        # My version looks a bit different from the tutorial and my map is
        # rotated by 90 degrees because of the way the map is stored. But
        # that doesn't matter.
        # And for some reason my textures are rotated or flipped.
        # This function needs to be fast, so there is minimal use of
        # Vector2 here.
        self.screen_buffer[:] = self.background_color
        for x, camera_x in enumerate(self.camera_x):
            ray_direction_x, ray_direction_y = self.view_direction + self.camera_plane * camera_x

            # Delta distance could be calculated with pythagoras but only
            # the ratio between them is important which simplifies
            # the equation here.
            delta_distance_x = abs(save_divide(1, ray_direction_x))
            delta_distance_y = abs(save_divide(1, ray_direction_y))

            if ray_direction_x < 0:
                step_x = -1
                side_distance_x = (self.position.x - self.map_position_x) * delta_distance_x
            else:
                step_x = 1
                side_distance_x = (self.map_position_x + 1 - self.position.x) * delta_distance_x
            if ray_direction_y < 0:
                step_y = -1
                side_distance_y = (self.position.y - self.map_position_y) * delta_distance_y
            else:
                step_y = 1
                side_distance_y = (self.map_position_y + 1 - self.position.y) * delta_distance_y

            # perform DDA
            wall_x = self.map_position_x
            wall_y = self.map_position_y
            side = None  # Was it a north/south or west/east wall?
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
            if side:
                wall_distance = (wall_y - self.position.y + (1 - step_y) / 2) / ray_direction_y
            else:
                wall_distance = (wall_x - self.position.x + (1 - step_x) / 2) / ray_direction_x

            # Calculate length of vertical stripe.
            line_height = int(self.h // wall_distance)
            line_height_half = line_height // 2
            line_top = max(self.screen_height_half - line_height_half, 0)
            line_bottom = min(
                self.screen_height_half + line_height_half,
                self.screen_bottom
            )

            # Calculate where exactly the wall was hit.
            if side:
                wall_x = self.position.x + wall_distance * ray_direction_x
            else:
                wall_x = self.position.y + wall_distance * ray_direction_y
            wall_x = wall_x % 1  # in the tutorial:  wallX -= floor((wallX))

            # x coordinate on the texture
            tex_x = int(wall_x * self.texture_width)
            if ((side == 0 and ray_direction_x > 0)
                    or (side == 1 and ray_direction_y < 0)):
                tex_x = self.texture_width - tex_x - 1

            # How much to increase the texture coordinate per screen pixel.
            step = self.texture_height / line_height
            # Starting texture coordinate.
            tex_pos = (line_top - self.h / 2 + line_height_half) * step
            for y in range(line_top, line_bottom):
                # Cast the texture coordinate to integer, and mask
                # with (texHeight - 1) in case of overflow
                tex_y = int(tex_pos % self.texture_height)
                tex_pos += step
                if side:
                    color = self.textures[wall_int][self.texture_height * tex_y + tex_x]
                else:
                    color = self.textures_dark[wall_int][self.texture_height * tex_y + tex_x]
                self.screen_buffer[x, y] = color

    def move_straight(self, sign, dt):
        # positive sign is forward, negative is backward
        self.move(*self.position + self.move_forward_velocity * sign * dt)

    def move_sideways(self, sign, dt):
        # positive sign is right, negative is left
        self.move(*self.position + self.move_right_velocity * sign * dt)

    def move(self, new_x, new_y):
        new_x_int = int(new_x)
        new_y_int = int(new_y)
        if self.world_map[new_y_int, new_x_int] == 0:
            self.position.update(new_x, new_y)
            self.map_position_x = new_x_int
            self.map_position_y = new_y_int

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
