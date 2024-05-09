import pygame


class GameConfig:
    ROW = 8
    COLUMN = 8
    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 800
    X_OFFSET = 100
    Y_OFFSET = 100
    SQUARE_SIZE = 75
    BOARD_SIZE = 8 * SQUARE_SIZE
    START_BUTTON_X = X_OFFSET + BOARD_SIZE + 100
    START_BUTTON_Y = Y_OFFSET + 120
    UNDO_BUTTON_X = X_OFFSET + BOARD_SIZE + 100
    UNDO_BUTTON_Y = Y_OFFSET + 3 * SQUARE_SIZE + 150
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 100
    MATERIAL_CHART_WIDTH = 20
    COLORS = {
        "WHITE": (255, 255, 255),
        "GRAY": (128, 128, 128),
        "RED": (127, 0, 0, 128),
        "DARK_RED": (255, 0, 0, 128),
        "GREEN": (0, 128, 0, 128),
        "BLACK": (0, 0, 0, 255),
        "LIGHT_GRAY": (169, 169, 169),
        "BEIGE": (255, 246, 231),
    }
    LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"]
    FPS = 30
    IMAGES = {}

    def load_images(self) -> None:
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
