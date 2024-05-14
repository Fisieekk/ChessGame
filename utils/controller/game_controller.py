from typing import Any, Optional, List
import pygame
from chess_engine import Map, Position, Piece
from utils.controller.game_config import GameConfig


class GameController:
    def __init__(self, config: GameConfig, game_map: Map):
        pygame.init()
        self.map = game_map
        self.config = config
        self.screen = pygame.display.set_mode(
            (self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)
        )
        self.scroll_offset = 0


    def draw_board(self) -> None:
        """
        Draws the board with the squares.
        :return: None
        """
        colors = [self.config.COLORS["WHITE"], self.config.COLORS["GRAY"]]
        pygame.draw.rect(
            self.screen,
            self.config.COLORS["BLACK"],
            (
                self.config.X_OFFSET - 1,
                self.config.Y_OFFSET - 1,
                self.config.BOARD_SIZE + 2,
                self.config.BOARD_SIZE + 2,
            ),
            2,
        )
        for r in range(self.config.ROW):
            for c in range(self.config.COLUMN):
                color = colors[((r + c) % 2)]
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        self.config.X_OFFSET + c * self.config.SQUARE_SIZE,
                        self.config.Y_OFFSET + r * self.config.SQUARE_SIZE,
                        self.config.SQUARE_SIZE,
                        self.config.SQUARE_SIZE,
                    ),
                )

    def draw_pieces(self) -> None:
        """
        Draws the pieces on the board.
        :return: None
        """
        for r in range(self.config.ROW):
            for c in range(self.config.COLUMN):
                current_piece = self.map.board[r][c]
                if current_piece is not None:
                    self.screen.blit(
                        self.config.IMAGES[current_piece.get_identificator()],
                        pygame.Rect(
                            self.config.X_OFFSET + c * self.config.SQUARE_SIZE,
                            self.config.Y_OFFSET + r * self.config.SQUARE_SIZE,
                            self.config.SQUARE_SIZE,
                            self.config.SQUARE_SIZE,
                        ),
                    )

    def draw_possible_moves(self, moves, attack_moves) -> None:
        """
        Draws the possible moves and attack moves on the board.
        :param moves: possible moves for the selected piece
        :param attack_moves: attack moves for the selected piece
        :return: None
        """
        for move in moves:
            r, c = (move.y, move.x)
            move_surface = pygame.Surface(
                (self.config.SQUARE_SIZE, self.config.SQUARE_SIZE), pygame.SRCALPHA
            )
            move_surface.fill(self.config.COLORS["GREEN"])
            self.screen.blit(
                move_surface,
                (
                    self.config.X_OFFSET + c * self.config.SQUARE_SIZE,
                    self.config.Y_OFFSET + r * self.config.SQUARE_SIZE,
                ),
            )

        for move in attack_moves:
            r, c = (move.y, move.x)
            attack_surface = pygame.Surface(
                (self.config.SQUARE_SIZE, self.config.SQUARE_SIZE), pygame.SRCALPHA
            )
            attack_surface.fill(self.config.COLORS["RED"])
            self.screen.blit(
                attack_surface,
                (
                    self.config.X_OFFSET + c * self.config.SQUARE_SIZE,
                    self.config.Y_OFFSET + r * self.config.SQUARE_SIZE,
                ),
            )

    def draw_checks(self) -> None:
        """
        Draws the checks on the board.
        :return: None
        """
        if self.map.check_white:
            r, c = self.map.white_king_position.y, self.map.white_king_position.x
        elif self.map.check_black:
            r, c = self.map.black_king_position.y, self.map.black_king_position.x
        else:
            return
        move_surface = pygame.Surface(
            (self.config.SQUARE_SIZE, self.config.SQUARE_SIZE), pygame.SRCALPHA
        )
        move_surface.fill(self.config.COLORS["DARK_RED"])
        self.screen.blit(
            move_surface,
            (
                self.config.X_OFFSET + c * self.config.SQUARE_SIZE,
                self.config.Y_OFFSET + r * self.config.SQUARE_SIZE,
            ),
        )

    def draw_message(self, color: Optional[str], message: Optional[str]) -> None:
        """
        Draws a message(when is checkmate or stalemate) on the board.
        :param color: color of the player who won, None if it is a stalemate
        :param message: message to be displayed(when is stalemate), None if it is a checkmate
        :return: None
        """
        if message is None:
            message = color[0].upper() + color[1:] + " won by checkmate"
        font = pygame.font.Font(None, 72)
        text = font.render(message, True, self.config.COLORS["GREEN"])

        text_rect = text.get_rect(
            center=(
                self.config.X_OFFSET + self.config.BOARD_SIZE // 2,
                self.config.Y_OFFSET + self.config.BOARD_SIZE // 2,
            )
        )
        self.screen.blit(text, text_rect)

    def draw_promotion_options(self, position: Position) -> list[tuple[Any, Any]]:
        """
        Draws the promotion options on the board.
        :param position: position where the promotion is happening
        :return: list of tuples with the identifier of the piece and the rectangle where it is drawn
        """
        c, r = position.x, position.y
        color, positions = ("b", [2, 3, 4, 5]) if r == 7 else ("w", [5, 4, 3, 2])
        r = -1.1 if r == 0 else 8.1
        rectangles = [
            pygame.Rect(
                self.config.X_OFFSET + c * self.config.SQUARE_SIZE,
                self.config.Y_OFFSET + r * self.config.SQUARE_SIZE,
                self.config.SQUARE_SIZE,
                self.config.SQUARE_SIZE,
            )
            for c in positions
        ]
        identifiers = [color + x for x in ["Q", "R", "B", "N"]]
        promoting_pieces = []
        for rectangle, identifier in zip(rectangles, identifiers):
            self.screen.blit(self.config.IMAGES[identifier], rectangle)
            promoting_pieces.append((identifier, rectangle))
        return promoting_pieces

    def drag_piece(self, x: int, y: int, selected_piece: Piece) -> None:
        """
        Draws the selected piece on the board.
        :param x: x position of the mouse
        :param y: y position of the mouse
        :param selected_piece: selected piece for the drag
        :return: None
        """
        if (
                0 < x - self.config.X_OFFSET < self.config.BOARD_SIZE
                and 0 < y - self.config.Y_OFFSET < self.config.BOARD_SIZE
        ):
            self.screen.blit(
                self.config.IMAGES[selected_piece.get_identificator()],
                (x - self.config.SQUARE_SIZE // 2, y - self.config.SQUARE_SIZE // 2),
            )

    def draw_reset_button(self) -> None:
        """
        Draws the reset button on the board.
        :return: None
        """
        font = pygame.font.SysFont(None, 64)
        text = font.render("RESET", True, self.config.COLORS["BLACK"])
        x, y, width, height = self.config.RESET_BUTTON
        text_rect = text.get_rect(
            center=(x + width // 2, y + height // 2),
        )

        mouse_pos = pygame.mouse.get_pos()
        is_mouse_over = pygame.Rect(self.config.RESET_BUTTON).collidepoint(mouse_pos)

        if is_mouse_over and pygame.mouse.get_pressed()[0]:
            button_color = self.config.COLORS["GRAY"]
        else:
            button_color = self.config.COLORS["LIGHT_GRAY"]

        pygame.draw.rect(
            self.screen,
            button_color,
            self.config.RESET_BUTTON,
            border_radius=self.config.BORDER_RADIUS
        )
        pygame.draw.rect(
            self.screen,
            self.config.COLORS["BLACK"],
            self.config.RESET_BUTTON,
            border_radius=self.config.BORDER_RADIUS,
            width=2)
        self.screen.blit(text, text_rect)

    def draw_utiles_rect(self) -> None:
        """
        Draws the rectangle for the utils on the board.
        :return: None
        """
        pygame.draw.rect(
            self.screen,
            self.config.COLORS["MENU_BACKGROUND"],
            self.config.UTILS_RECTANGLE,
            border_radius=self.config.BORDER_RADIUS
        )   

    def draw_moves_list(self):
        y_offset = 5 - self.scroll_offset
        for move in self.map.history:
            move_surf = self.config.FONT.render(move, True, (255, 255, 255))
            move_rect = move_surf.get_rect(topleft=(self.config.HISTORY_RECTANGLE.x + 5, self.config.HISTORY_RECTANGLE.y + y_offset))
            self.screen.blit(move_surf, move_rect)
            y_offset += move_surf.get_height() + 5

    def draw_material_diff(self, evaluation: float) -> None:
        """
        Draws the material difference between the two players(chart on the left side of the board).
        Will be updated to show stockfish evaluation in the future.
        :param evaluation: evaluation of the position, positive if white is winning, negative if black is winning
        :return: None
        """
        ratio = (-evaluation / 100 + 10) / 20
        b_x, b_y = (
            self.config.X_OFFSET - 2 * self.config.MATERIAL_CHART_WIDTH,
            self.config.Y_OFFSET,
        )
        w_x, w_y = b_x, b_y + int(ratio * self.config.BOARD_SIZE)
        b_x_diff, b_y_diff = self.config.MATERIAL_CHART_WIDTH, w_y
        w_x_diff, w_y_diff = (
            self.config.MATERIAL_CHART_WIDTH,
            self.config.Y_OFFSET + self.config.BOARD_SIZE - w_y,
        )
        pygame.draw.rect(self.screen, (0, 0, 0), (b_x, b_y, b_x_diff, b_y_diff))

        pygame.draw.rect(self.screen, (255, 255, 255), (b_x, w_y, w_x_diff, w_y_diff))

        text = self.config.EVAL_FONT.render(str(evaluation/100), True, self.config.COLORS["WHITE"])
        text_rect = text.get_rect(
            center=(b_x + b_x_diff//2, self.config.Y_OFFSET+self.config.BOARD_SIZE + 25),
        )
        self.screen.blit(text, text_rect)

    def draw_utils(self, evaluation: float) -> None:
        """
        Draws the reset button, undo button and material difference chart on the board.
        :return: None
        """
        self.draw_reset_button()
        self.draw_utiles_rect()
        self.draw_material_diff(evaluation)

    def update_screen(self, evaluation: float) -> None:
        """
        Updates the screen with the new board state.
        :param evaluation: evaluation of the position, positive if white is winning, negative if black is winning
        :return: None
        """
        self.screen.fill(self.config.COLORS["APP_BACKGROUND"])
        self.draw_board()
        self.draw_pieces()
        self.draw_utils(evaluation)
