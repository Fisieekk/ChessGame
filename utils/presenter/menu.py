from typing import Optional
import pygame
import sys
from chess_engine import Position
from utils.presenter.menu_config import MenuConfig


class Menu:
    def __init__(self):
        pygame.init()
        self.config = MenuConfig()
        self.screen = pygame.display.set_mode((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        self.buttons = []
        self.enemy_type = None

    def draw_menu_background(self) -> None:
        """
        Draw the background of the menu rectangle with rounded corners
        :return: None
        """
        button_rect = pygame.Rect(self.config.X_OFFSET, self.config.Y_OFFSET, self.config.MENU_WIDTH,
                                  self.config.MENU_HEIGHT)
        pygame.draw.rect(self.screen, self.config.COLORS["MENU_BACKGROUND"], button_rect,
                         border_radius=self.config.BORDER_RADIUS)

    def draw_buttons(self) -> None:
        """
        Draw the buttons for the menu
        :return: None
        """
        for text, (x, y, width, height) in self.config.GAME_TYPE_BUTTONS.items():
            button_rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(self.screen, self.config.COLORS["BUTTON_BACKGROUND"], button_rect,
                             border_radius=self.config.BORDER_RADIUS)
            if len(self.buttons) < len(self.config.GAME_TYPE_BUTTONS):
                self.buttons.append((button_rect, text))

            text_surf = self.config.FONT.render(text, True, self.config.COLORS["WHITE"])
            text_rect = text_surf.get_rect(center=button_rect.center)
            self.screen.blit(text_surf, text_rect)

    def draw_enemy_chose_menu(self) -> None:
        """
        Draw the menu to chose between playing with a computer or onboard
        :return: None
        """
        self.draw_menu_background()
        self.draw_buttons()

    def handle_enemy_chose_menu(self, x: int, y: int) -> None:
        """
        Handle the user input for the menu
        :param x: x coordinate of the mouse click
        :param y: y coordinate of the mouse click
        :return: None
        """
        for button_rect, action in self.buttons:
            if button_rect.collidepoint(x, y):
                self.enemy_type = action.split()[-1] # Get the last word of the button text(onboard/computer/game)
                print(f"Selected game mode: {self.enemy_type}")  # Debug print

    def update_screen(self) -> None:
        """
        Update the screen with the current state of the menu
        :return: None
        """
        self.screen.fill(self.config.COLORS["APP_BACKGROUND"])
        self.draw_enemy_chose_menu()
        pygame.display.flip()

    def main(self) -> Optional[str]:
        """
        Main loop for the menu
        :return:
        """
        pygame.display.set_caption('Menu')
        while self.enemy_type is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_enemy_chose_menu(*event.pos)
            self.update_screen()
        return self.enemy_type
