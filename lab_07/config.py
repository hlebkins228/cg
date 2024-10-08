MAIN_COLOUR = "#616161"

MAIN_FRAME_COLOR = "#313335"
MAIN_COLOUR_LABEL_BG = "#CC2342"
MAIN_COLOUR_LABEL_TEXT = "white"

CANVAS_COLOUR = "white"
LINE_COLOUR = "black"
RESULT_COLOUR = "red"
CLIPPER_COLOUR = "blue"

COLUMNS = 26

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = int(WINDOW_WIDTH * (1000 / 1900))

DATA_SITUATION = 1/4
BORDERS_SPACE = 10

DATA_FRAME_WIGHT = WINDOW_WIDTH * DATA_SITUATION - BORDERS_SPACE
DATA_FRAME_HEIGHT = WINDOW_HEIGHT - 2 * BORDERS_SPACE

CANVAS_SITUATION = 1 - DATA_SITUATION
CANVAS_WIDTH = WINDOW_WIDTH * CANVAS_SITUATION - 2 * BORDERS_SPACE
CANVAS_HEIGHT = WINDOW_HEIGHT - 2 * BORDERS_SPACE
