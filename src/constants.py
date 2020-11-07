SMALL_DISPLAY_WIDTH = 600
SMALL_DISPLAY_HEIGHT = 450
SMALL_DISPLAY_SIZE = (SMALL_DISPLAY_WIDTH, SMALL_DISPLAY_HEIGHT)
MAGNIFICATION = 2
MAIN_DISPLAY_WIDTH = SMALL_DISPLAY_WIDTH * MAGNIFICATION
MAIN_DISPLAY_HEIGHT = SMALL_DISPLAY_HEIGHT * MAGNIFICATION
MAIN_DISPLAY_SIZE = (MAIN_DISPLAY_WIDTH, MAIN_DISPLAY_HEIGHT)
FPS = 60
DT_LIMIT = 2 / FPS  # half the time of one normal frame

TURN_LEFT = "turn left"
TURN_RIGHT = "turn right"
MOVE_FORWARD = "move forward"
MOVE_BACKWARD = "move backward"
TOGGLE_DEV_OVERLAY = "toggle dev overlay"

DEFAULT_OPTIONS = {
    "controls": {
        TURN_LEFT: "a",
        TURN_RIGHT:  "d",
        MOVE_FORWARD: "w",
        MOVE_BACKWARD: "s",
        TOGGLE_DEV_OVERLAY: "f1"
    },
    "camera": {
        "fov_degrees": 90,
        "move_speed": 5,
        "rotate_speed": 3
    }
}

BACKGROUND_COLOR = (32, 32, 32)
