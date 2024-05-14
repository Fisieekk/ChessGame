import pygame


class MenuConfig:
    def __init__(self):
        self.WINDOW_WIDTH = 1300
        self.WINDOW_HEIGHT = 800
        self.MENU_WIDTH = 800
        self.MENU_HEIGHT = 500
        self.X_OFFSET = 250
        self.Y_OFFSET = 150
        self.GAME_MODES = {
            "Bullet": ["1+0", "2+1"],
            "Blitz": ["3+0", "3+2", "5+0", "5+3"],
            "Rapid": ["10+0", "10+5", "15+10"],
            "Classical": ["30+0", "30+20"],
            "Custom": ["Custom time settings"]
        }
        self.COLORS = {
            "WHITE": (255, 255, 255),
            "GRAY": (128, 128, 128),
            "RED": (127, 0, 0, 128),
            "DARK_RED": (255, 0, 0, 96),
            "GREEN": (0, 128, 0, 96),
            "BLACK": (0, 0, 0, 255),
            "LIGHT_GRAY": (169, 169, 169),
            "BEIGE": (255, 246, 231),
            "APP_BACKGROUND": (20, 20, 20),
            "MENU_BACKGROUND": (30, 30, 30),
            "BUTTON_BACKGROUND": (50, 50, 50),
            "BUTTON_TEXT": (255, 255, 255),
        }
        self.GAME_TYPE_BUTTONS = {
            "Play onboard": (self.X_OFFSET + 150, self.Y_OFFSET + 50, 500, 100),
            "Play with computer": (self.X_OFFSET + 150, self.Y_OFFSET + 200, 500, 100),
            "Quit": (self.X_OFFSET + 150, self.Y_OFFSET + 350, 500, 100),
        }

        self.COLOR_CHOICE_BUTTONS = {
            "Play as white": (self.X_OFFSET + 150, self.Y_OFFSET + 50, 500, 100),
            "Play as black": (self.X_OFFSET + 150, self.Y_OFFSET + 200, 500, 100),
            "Back": (self.X_OFFSET + 150, self.Y_OFFSET + 350, 500, 100),
        }

        self.FONT = pygame.font.Font(None, 36)
        self.BORDER_RADIUS = 10
