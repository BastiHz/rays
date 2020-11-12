# Note about FOV and appearance of the walls:
# The aspect ratio of the walls depends on the fov, the aspect ratio of the
# window, and the value of h in this line: line_height = h / wall_distance.
# They look square when the fov is 66°, the aspect ratio is 4:3 and h is
# the display height. Consider this when changing any one of those three values.


import math


SMALL_DISPLAY_WIDTH = 640 * 2
SMALL_DISPLAY_HEIGHT = 480 * 2
assert SMALL_DISPLAY_WIDTH * 3/4 == SMALL_DISPLAY_HEIGHT
SMALL_DISPLAY_SIZE = (SMALL_DISPLAY_WIDTH, SMALL_DISPLAY_HEIGHT)
DISPLAY_MAGNIFICATION = 2 // 2
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


# ATTENTION: Do not put constants from above into the default options below.
#  Because it has happened multiple times that I changed a constant and forgot
#  to regenerate the options file which led to weird bugs.
DEFAULT_OPTIONS = {
    "controls": {
        MOVE_FORWARD: "w",
        MOVE_LEFT: "a",
        MOVE_BACKWARD: "s",
        MOVE_RIGHT: "d",
        ROTATE_LEFT: "q",
        ROTATE_RIGHT: "e",
        PAUSE: "p",
        TOGGLE_DEV_OVERLAY: "f1"
    },
    "camera": {
        "fov_degrees": 66,
        "move_speed": 5,  # squares / s
        "rotate_speed_keyboard": math.pi,  # radians / s
        "rotate_speed_mouse": math.pi,  # radians / SMALL_WINDOW_WIDTH
        "rotate_speed_mouse_multiplier": 1.5
    }
}
