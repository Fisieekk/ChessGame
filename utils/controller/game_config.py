import pygame


class GameConfig:
    pygame.init()
    ROW = 8
    COLUMN = 8
    WINDOW_WIDTH = 1300
    WINDOW_HEIGHT = 800
    X_OFFSET = 100
    Y_OFFSET = 100
    SQUARE_SIZE = 75
    BOARD_SIZE = 8 * SQUARE_SIZE
    MATERIAL_CHART_WIDTH = 20
    COLORS = {
        "WHITE": (255, 255, 255),
        "GRAY": (128, 128, 128),
        "RED": (127, 0, 0, 128),
        "DARK_RED": (255, 0, 0, 96),
        "GREEN": (0, 128, 0, 96),
        "BLACK": (0, 0, 0, 255),
        "LIGHT_GRAY": (169, 169, 169),
        "BEIGE": (255, 246, 231),
        "APP_BACKGROUND": (20, 20, 20),
        "MENU_BACKGROUND": (40, 40, 40),
        "MESSAGE_BACKGROUND": (50, 50, 50),
        "BUTTON_BACKGROUND": (60, 60, 60),
        "WHITE_MOVE_BACKGROUND": (70, 70, 70),
        "MOVE_NUMBER_BACKGROUND": (80, 80, 80),
        "BLACK_MOVE_BACKGROUND": (90, 90, 90),
    }
    LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"]
    FPS = 120
    IMAGES = {}
    UTILS_RECTANGLE = (X_OFFSET + BOARD_SIZE + 100, Y_OFFSET, 400, 520)
    (
        x,
        y,
        width,
        height,
    ) = UTILS_RECTANGLE
    RESET_BUTTON = (x, y + height + 20, 400, 50)
    HISTORY_RECTANGLES = (
        (x + 10, y + 10, 90, 50),
        (x + 100, y + 10, 145, 50),
        (x + 245, y + 10, 145, 50),
    )
    BORDER_RADIUS = 10
    FONT = pygame.font.Font(None, 32)
    EVAL_FONT = pygame.font.Font(None, 24)

    def load_images(self) -> None:
        """
        Load the images of the pieces and store them in the IMAGES dictionary.
        :return: None
        """
        pieces = [
            "wR",
            "wN",
            "wB",
            "wQ",
            "wK",
            "wP",
            "bR",
            "bN",
            "bB",
            "bQ",
            "bK",
            "bP",
        ]
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(
                pygame.image.load("utils/images/" + piece + ".png"),
                (self.SQUARE_SIZE, self.SQUARE_SIZE),
            )
