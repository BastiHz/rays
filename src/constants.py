# Note about FOV and appearance of the walls:
# The aspect ratio of the walls depends on the fov, the aspect ratio of the
# window, and the value of h in this line: line_height = h / wall_distance.
# They look square when the fov is 66°, the aspect ratio is 4:3 and h is
# the display height. Consider this when changing any one of those three values.


import math


SMALL_DISPLAY_WIDTH = 640
SMALL_DISPLAY_HEIGHT = 480
# FOV and cast() are adjusted so that a window ratio of 4:3 looks best.
assert SMALL_DISPLAY_WIDTH * 3/4 == SMALL_DISPLAY_HEIGHT
# Window height must be even or else the center row of pixels is neither floor
# nor ceiling.
assert SMALL_DISPLAY_HEIGHT % 2 == 0
SMALL_DISPLAY_SIZE = (SMALL_DISPLAY_WIDTH, SMALL_DISPLAY_HEIGHT)
DISPLAY_MAGNIFICATION = 2
MAIN_DISPLAY_WIDTH = SMALL_DISPLAY_WIDTH * DISPLAY_MAGNIFICATION
MAIN_DISPLAY_HEIGHT = SMALL_DISPLAY_HEIGHT * DISPLAY_MAGNIFICATION
MAIN_DISPLAY_SIZE = (MAIN_DISPLAY_WIDTH, MAIN_DISPLAY_HEIGHT)

FPS = 60
DT_LIMIT = 2 / FPS  # half the time of one normal frame

MOVE_FORWARD = "move forward"
MOVE_BACKWARD = "move backward"
MOVE_LEFT = "move left"
MOVE_RIGHT = "move right"
ROTATE_LEFT = "rotate left"
ROTATE_RIGHT = "rotate right"
TOGGLE_DEV_OVERLAY = "toggle dev overlay"
PAUSE = "pause"
