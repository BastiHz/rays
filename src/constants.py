import math


SMALL_DISPLAY_WIDTH = 600
SMALL_DISPLAY_HEIGHT = 450
SMALL_DISPLAY_SIZE = (SMALL_DISPLAY_WIDTH, SMALL_DISPLAY_HEIGHT)
DISPLAY_MAGNIFICATION = 2
MAIN_DISPLAY_SIZE = (
    SMALL_DISPLAY_WIDTH * DISPLAY_MAGNIFICATION,
    SMALL_DISPLAY_HEIGHT * DISPLAY_MAGNIFICATION
)
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
        "rotate_speed_mouse": math.pi / SMALL_DISPLAY_WIDTH,  # radians / pixel
        "rotate_speed_mouse_multiplier": 1.5
    }
}

BACKGROUND_COLOR = (32, 32, 32)
