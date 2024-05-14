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
        self.game_type = None
        self.choosing_color = False
        self.chosen_color = None
        self.config_complete = False

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
        button_config = self.config.COLOR_CHOICE_BUTTONS if self.choosing_color else self.config.GAME_TYPE_BUTTONS

        for text, (x, y, width, height) in button_config.items():
            button_rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(self.screen, self.config.COLORS["BUTTON_BACKGROUND"], button_rect,
                             border_radius=self.config.BORDER_RADIUS)
            if len(self.buttons) < len(button_config):
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
                if action == "Play with computer":
                    self.game_type = "computer"
                    self.choosing_color = True
                    self.buttons.clear()
                elif action in ["Play as white", "Play as black"]:
                    self.chosen_color = action.split()[-1]  # Store chosen color
                    self.config_complete = True
                elif action == "Back":
                    self.choosing_color = False
                    self.buttons.clear()
                else:
                    self.game_type = action.split()[-1]  # Get the last word of the button text(onboard/quit)
                    self.config_complete = True
                print(f"Game type: {self.game_type}")


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
        while not self.config_complete:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_enemy_chose_menu(*event.pos)
            self.update_screen()
        return self.game_type
