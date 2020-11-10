# This is the part of the tutorial with simple textured surfaces, before
# the part where I load textures from image files.


import numpy


# This stuff is mostly just copied from the tutorial:
# https://lodev.org/cgtutor/raycasting.html#Textured_Raycaster

def generate_textures(width, height):
    # TODO: For some reason the textures are vectors in the tutorial, not
    #  2d arrays. Maybe change that.
    textures = [numpy.zeros((width, height), dtype=int) for _ in range(8)]
    for x in range(width):
        for y in range(height):
            xor_color = (x * 256 // width) ^ (y * 256 // height)
            # x_color = x * 256 // width
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
    return textures
