# This is the part of the tutorial with simple textured surfaces, before
# the part where I load textures from image files.


import numpy as np
import pygame


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


def generate_walls(width, height):
    # This stuff is mostly just copied from the tutorial:
    # https://lodev.org/cgtutor/raycasting.html#Textured_Raycaster
    textures = [np.zeros((width, height), int) for _ in range(8)]
    for x in range(width):
        for y in range(height):
            xor_color = (x * 256 // width) ^ (y * 256 // height)
            y_color = y * 256 // height
            xy_color = y * 128 // height + x * 128 // width
            textures[0][x, y] = 65536 * 254 * (x != y and x != width - y)  # flat red texture with black cross
            textures[1][x, y] = xy_color + 256 * xy_color + 65536 * xy_color  # sloped greyscale
            textures[2][x, y] = 256 * xy_color + 65536 * xy_color  # sloped yellow gradient
            textures[3][x, y] = xor_color + 256 * xor_color + 65536 * xor_color  # xor greyscale
            textures[4][x, y] = 256 * xor_color  # xor green
            textures[5][x, y] = 65536 * 192 * (x % 16 and y % 16)  # red bricks
            textures[6][x, y] = 65536 * y_color  # red gradient
            textures[7][x, y] = 128 + 256 * 128 + 65536 * 128  # flat grey texture
    # Flip the textures horizontally so they look like in the examples pictures
    # in the tutorial.
    return [np.flip(t, axis=0) for t in textures]


def generate_floor(width, height):
    floor = pygame.Surface((width, height))
    floor.fill((32, 32, 32))
    pygame.draw.rect(floor, (32, 32, 64), floor.get_rect(), 10)
    return pygame.surfarray.array2d(floor)


def generate_ceiling(width, height):
    ceiling = pygame.Surface((width, height))
    ceiling.fill((250, 250, 250))
    pygame.draw.rect(ceiling, (64, 64, 64), ceiling.get_rect(), 2)
    center = (width / 2, height / 2)
    pygame.draw.circle(ceiling, (128, 128, 128), center, 6, 1)
    pygame.draw.circle(ceiling, (255, 255, 128), center, 5)
    return pygame.surfarray.array2d(ceiling)
