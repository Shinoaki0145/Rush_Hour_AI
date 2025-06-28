import os

# Coordinate of board
MATRIX = [[(278, 278), (355, 278), (432, 278), (509, 278), (586, 278), (663, 278)],
          [(278, 355), (355, 355), (432, 355), (509, 355), (586, 355), (663, 355)],
          [(278, 432), (355, 432), (432, 432), (509, 432), (586, 432), (663, 432)],
          [(278, 509), (355, 509), (432, 509), (509, 509), (586, 509), (663, 509)],
          [(278, 586), (355, 586), (432, 586), (509, 586), (586, 586), (663, 586)],
          [(278, 663), (355, 663), (432, 663), (509, 663), (586, 663), (663, 663)]]

VALID_MATRIX = [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]]

END_COORDINATE = (664, 432)

MAP_SIZE = (1920, 1920)
HEIGHT_DEFAULT = 1020
HEADER_BAR = 60
SQUARE_SIZE_DEFAULT = 77

WHITE = (255, 255, 255)
BLUE_LIGHT = (74, 158, 255)
BACKGROUND = (240, 240, 240)

MOVE_SPEED = 3
STEP_DELAY = 500

SRC_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
ASSET_PATH = SRC_PATH + "../Asset/"
BUTTON_PATH = ASSET_PATH + "Button/"
CAR_PATH = ASSET_PATH + "Car/"
DISPLAY_PATH = ASSET_PATH + "Display/"
FONT_PATH = ASSET_PATH + "Font/"

TARGET_CAR_PATH = CAR_PATH + "car_target.png"

BACKGROUND_PATH = ASSET_PATH + "Background/bg_game.jpg"

FONT = ASSET_PATH + "Font/FredokaOne-Regular.ttf"

def clear_valid_matrix():
    for i in range(len(VALID_MATRIX)):
        for j in range(len(VALID_MATRIX[0])):
            VALID_MATRIX[i][j] = 0
