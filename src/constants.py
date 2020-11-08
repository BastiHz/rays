SMALL_DISPLAY_WIDTH = 600
SMALL_DISPLAY_HEIGHT = 450
SMALL_DISPLAY_SIZE = (SMALL_DISPLAY_WIDTH, SMALL_DISPLAY_HEIGHT)
MAGNIFICATION = 2
MAIN_DISPLAY_WIDTH = SMALL_DISPLAY_WIDTH * MAGNIFICATION
MAIN_DISPLAY_HEIGHT = SMALL_DISPLAY_HEIGHT * MAGNIFICATION
MAIN_DISPLAY_SIZE = (MAIN_DISPLAY_WIDTH, MAIN_DISPLAY_HEIGHT)
FPS = 60
DT_LIMIT = 2 / FPS  # half the time of one normal frame

MOVE_FORWARD = "move forward"
MOVE_BACKWARD = "move backward"
MOVE_LEFT = "move left"
MOVE_RIGHT = "move right"
TURN_LEFT = "rotate left"
TURN_RIGHT = "rotate right"
TOGGLE_DEV_OVERLAY = "toggle dev overlay"

DEFAULT_OPTIONS = {
    "controls": {
        MOVE_FORWARD: "w",
        MOVE_LEFT: "a",
        MOVE_BACKWARD: "s",
        MOVE_RIGHT: "d",
        TURN_LEFT: "q",
        TURN_RIGHT: "e",
        TOGGLE_DEV_OVERLAY: "f1"
    },
    "camera": {
        "fov_degrees": 90,
        "move_speed": 5,
        "rotate_speed": 3
    }
}

BACKGROUND_COLOR = (32, 32, 32)