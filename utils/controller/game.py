from time import sleep

import pygame
from chess import engine
from chess_engine import *
from .game_config import GameConfig
from .game_controller import GameController
from stockfish import Stockfish
from ..presenter.menu import Menu


class Game:
    def __init__(self):
        self.config = GameConfig()
        self.menu = Menu()
        self.map = Map(8, 8)
        self.controller = GameController(self.config, self.map)
        self.history = []
        self.captured_pieces = []
        self.moves = None
        self.attack_moves = None
        self.running = True
        self.selected_piece = None
        self.original_pos = None
        self.mouse_down = False
        self.config.LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.fps_counter = 0
        self.mate = False
        self.stalemate = False
        self.promoting_pieces = None
        self.config.load_images()
        self.stockfish_path = (
            r".\.\chess_engine\stockfish\stockfish-windows-x86-64-avx2.exe"
        )
        self.engine = Stockfish(
            path=self.stockfish_path
        )
        self.game_type = None
        self.player_color = "white"
        self.engine_color = "black"

    def reinitialize(self) -> None:
        """
        Reinitialize the game after clicking the reset button
        :return: None
        """
        self.map = Map(8, 8)
        self.controller = GameController(self.config, self.map)
        self.history = []
        self.captured_pieces = []
        self.moves = None
        self.attack_moves = None
        self.running = True
        self.selected_piece = None
        self.original_pos = None
        self.mouse_down = False
        self.fps_counter = 0
        self.mate = False
        self.stalemate = False
        self.promoting_pieces = None
        self.engine = Stockfish(path=self.stockfish_path)

    def handle_promotion(self, x: int, y: int) -> bool:
        """
        Handle the promotion of a pawn
        :param x: x coordinate of the mouse
        :param y: y coordinate of the mouse
        :return: None
        """
        for identifier, current_position in self.promoting_pieces:
            if current_position.collidepoint(x, y):
                new_position = Position(x=0, y=0)
                new_position.from_string_to_map(self.map.history[-1][2:])
                print("New position: ", new_position)
                self.map.change_piece(new_position, identifier)
                return True
        return False

    def select_piece(self, x: int, y: int) -> None:
        """
        Select a piece on the board to move
        :param x: x coordinate of the mouse
        :param y: y coordinate of the mouse
        :return: None
        """
        if (
            0 < x - self.config.X_OFFSET < self.config.BOARD_SIZE
            and 0 < y - self.config.Y_OFFSET < self.config.BOARD_SIZE
        ):
            row, col = (x - self.config.X_OFFSET) // self.config.SQUARE_SIZE, (
                y - self.config.Y_OFFSET
            ) // self.config.SQUARE_SIZE
            if (
                self.map.board[col][row]
                and self.map.board[col][row].color == self.map.curr_player
            ):
                self.selected_piece = self.map.board[col][row]
                self.original_pos = Position(x=row, y=col)
                self.mouse_down = True

    def update_possible_moves(self) -> None:
        """
        Update the possible moves if we have selected a piece
        :return: None
        """
        if self.selected_piece:
            self.moves, self.attack_moves = self.selected_piece.can_move(self.map)
            if type(self.selected_piece) is King:
                self.moves, self.attack_moves = self.map.castle(
                    self.moves, self.attack_moves, self.selected_piece
                )
            self.moves, self.attack_moves = self.map.preventer(
                self.moves, self.attack_moves, self.selected_piece
            )
        # print("Moves: ", self.moves)
        # print("Attack moves: ", self.attack_moves)

    def en_passant_verification(self, new_position: Position) -> bool:
        """
        Verify if the move is an en passant move.
        :param new_position: new position of the piece
        :return: True if it is an en passant move, False otherwise
        """
        return (
            self.map.last_move
            and abs(self.map.last_move[1].y - self.map.last_move[0].y) == 2
            and type(self.map.board[self.original_pos.y][self.original_pos.x]) is Pawn
            and new_position in self.attack_moves
            and type(self.map.board[self.original_pos.y][new_position.x]) is Pawn
            and self.map.board[self.original_pos.y][new_position.x].color
            != self.map.curr_player
        )

    def en_passant_move(self, new_position: Position) -> None:
        """
        Make an en passant move
        :param new_position: new position of the piece
        :return: None
        """
        self.captured_pieces.append(
            self.map.board[self.original_pos.y][new_position.x].get_identificator()
        )
        self.map.evaluate_captured_piece(
            self.map.board[self.original_pos.y][new_position.x]
        )
        self.map.en_passant_move(
            self.original_pos, Position(x=new_position.x, y=new_position.y)
        )

    def move(self, new_position: Position) -> None:
        """
        Make a move on the board
        :param new_position: new_position of the piece
        :return: None
        """
        if self.map.board[new_position.y][new_position.x]:
            self.captured_pieces.append(
                self.map.board[new_position.y][new_position.x].get_identificator()
            )
            self.map.evaluate_captured_piece(
                self.map.board[new_position.y][new_position.x]
            )

        self.map.move(self.original_pos, Position(x=new_position.x, y=new_position.y))

    def choose_type_of_move(self, x: int, y: int) -> None:
        """
        Choose the type of move to make
        :param x: x coordinate of the mouse
        :param y: y coordinate of the mouse
        :return: None
        """
        if (
            0 < x - self.config.X_OFFSET < self.config.BOARD_SIZE
            and 0 < y - self.config.Y_OFFSET < self.config.BOARD_SIZE
        ):
            new_position = Position(
                x=((x - self.config.X_OFFSET) // self.config.SQUARE_SIZE),
                y=((y - self.config.Y_OFFSET) // self.config.SQUARE_SIZE),
            )
            if new_position in self.moves or new_position in self.attack_moves:
                if (
                    self.original_pos.x != new_position.x
                    or self.original_pos.y != new_position.y
                ):
                    if self.en_passant_verification(new_position):
                        self.en_passant_move(new_position)
                    else:
                        self.move(new_position)
                        """
                        print("Captured value: ")
                        print(
                        "White: ",
                        self.map.white_captured_value,
                        " Black: ",
                        self.map.black_captured_value,
                    )
                        """

                    self.selected_piece.last_move = (
                        self.map.history[-1] if self.map.history else None
                    )
                    self.map.curr_player = (
                        "white" if self.map.curr_player == "black" else "black"
                    )

                if not self.map.promoting_piece:
                    last_move = self.map.history[-1]
                    self.engine.make_moves_from_current_position([last_move])

        self.map.check(self.map.curr_player)
        self.mate = self.map.calculate_mate()
        self.stalemate = self.map.calculate_stalemate()
        self.selected_piece = None
        self.moves, self.attack_moves = None, None
        self.mouse_down = False

    def new_game_button_clicked(self, x, y) -> None:
        """
        Reset the game if the reset button is clicked
        :param x: x coordinate of the mouse
        :param y: y coordinate of the mouse
        :return: None
        """
        button_rect = pygame.Rect(self.config.RESET_BUTTON)
        if button_rect.collidepoint(x, y):
            self.reinitialize()

    def main(self) -> None:
        """
        Main function to run the game and handle the events
        :return: None
        """
        pygame.init()
        pygame.font.init()
        self.game_type, elo = self.menu.main()
        if self.game_type == "Quit":
            pygame.quit()
            return
        elif self.game_type == "computer":
            self.player_color = self.menu.chosen_color
            self.engine_color = "black" if self.player_color == "white" else "white"
            self.engine.set_skill_level(1)
            self.engine.set_elo_rating(elo)

        timer = pygame.time.Clock()
        pygame.display.set_caption("Chess App")
        self.engine.set_position([])
        evaluation = self.engine.get_evaluation()

        while self.running:
            timer.tick(self.config.FPS)


            # if self.fps_counter % 15 == 0:  # every 15 frames to not kill the CPU
            #     evaluation = self.engine.get_evaluation()
            self.controller.update_screen(evaluation["value"])
            self.fps_counter += 1

            if (
                self.game_type == "computer"
                and self.map.curr_player == self.engine_color and not self.mate and not self.stalemate
            ):
                pygame.display.flip() # might seem redundant but prevents user move lag
                result = self.engine.get_best_move()
                sleep(0.2)
                self.map.make_engine_move(result, self.player_color, self.engine_color)
                self.engine.make_moves_from_current_position([result])
                self.map.check(self.map.curr_player)
                self.mate = self.map.calculate_mate()
                self.stalemate = self.map.calculate_stalemate()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if (
                    self.map.curr_player == self.player_color
                    or self.game_type == "onboard"
                ):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        self.new_game_button_clicked(x, y)

                    if not self.mate and not self.stalemate:
                        if not self.map.promoting_piece:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                x, y = pygame.mouse.get_pos()
                                self.select_piece(x, y)
                                self.update_possible_moves()

                            if (
                                event.type == pygame.MOUSEBUTTONUP
                                and self.selected_piece
                            ):
                                x, y = pygame.mouse.get_pos()
                                self.choose_type_of_move(x, y)

            if self.map.promoting_piece:
                promoting_piece_position = self.map.promoting_piece.position
                self.promoting_pieces = self.controller.draw_promotion_options(
                    promoting_piece_position
                )
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.handle_promotion(x, y):
                        last_move = self.map.history[-1]
                        self.engine.make_moves_from_current_position([last_move])
                        self.map.promoting_piece = None
                        self.map.check(self.map.curr_player)
                        self.mate = self.map.calculate_mate()
                        self.stalemate = self.map.calculate_stalemate()
            if self.mate:
                self.controller.draw_message(
                    "white" if self.map.curr_player == "black" else "black",
                    None,
                    self.game_type,
                    self.player_color,
                )

            elif self.stalemate:
                self.controller.draw_message(None, "Stalemate", None, None)

                # dragging piece
            if self.mouse_down and self.selected_piece:
                x, y = pygame.mouse.get_pos()
                self.controller.drag_piece(x, y, self.selected_piece)

            if self.mouse_down:
                self.controller.draw_possible_moves(self.moves, self.attack_moves)

            if self.map.check_white or self.map.check_black:
                self.controller.draw_checks()

            if self.fps_counter % 100 == 0:
                print(self.map.history)

            pygame.display.flip()

        pygame.quit()
