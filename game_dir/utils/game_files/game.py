import os
from typing import List, Dict

import pygame
import json
from datetime import datetime
from time import sleep
from stockfish import Stockfish
from chess_engine.map import Map
from chess_engine.pieces.king import King
from chess_engine.pieces.pawn import Pawn
from chess_engine.position import Position
from .game_config import GameConfig
from .game_controller import GameController
from utils.menu_files.menu import Menu
from utils.score_database import upload_new


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
        self.fps_counter = 0
        self.mate = False
        self.stalemate = False
        self.promoting_pieces = None
        self.config.load_images()
        self.stockfish_path = (
            r"game_dir\chess_engine\stockfish\stockfish-windows-x86-64-avx2.exe"
        )
        self.engine = Stockfish(path=self.stockfish_path)
        self.eval_engine = Stockfish(path=self.stockfish_path)
        self.game_type = None
        self.elo = None
        self.player_color = "white"
        self.engine_color = "black"
        self.game_time_start = None
        self.game_time_stop = None
        self.game_saved = False

    def reinitialize(self) -> None:
        """
        Reinitialize the game state
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
                # print("New position: ", new_position)
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
                    self.eval_engine.make_moves_from_current_position([last_move])

        self.map.check(self.map.curr_player)
        self.mate = self.map.calculate_mate()
        self.stalemate = self.map.calculate_stalemate()
        self.selected_piece = None
        self.moves, self.attack_moves = None, None
        self.mouse_down = False

    def new_game_button_clicked(self, x, y) -> int:
        """
        Check if we clicked the new game button
        :param x: x coordinate of the mouse
        :param y: y coordinate of the mouse
        :return: 1 if we clicked new game, 0 elsewhere
        """
        button_rect = pygame.Rect(self.config.RESET_BUTTON)
        if button_rect.collidepoint(x, y):
            return 1
        return 0

    def handle_menu(self) -> int:
        """
        Method to show and handle a menu.
        :return: 1 if we choose to quit, 0 elsewhere
        """
        self.game_type, self.elo = self.menu.main()
        if self.game_type == "Quit":
            return 1
        elif self.game_type == "computer":
            self.player_color = self.menu.chosen_color
            self.engine_color = "black" if self.player_color == "white" else "white"
            self.engine.set_skill_level(1)
            self.engine.set_elo_rating(self.elo)

        return 0

    def read_json(self) -> List[Dict]:
        """
        Read a json file which contains a list of past games, create it if it does not exist
        :return: list with the json content
        """
        if not os.path.exists(self.config.JSON_PATH):
            with open(self.config.JSON_PATH, "w") as file:
                json.dump([], file)

        with open(self.config.JSON_PATH, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

        return data

    def write_json(self, data: List[Dict]) -> None:
        """
        Write a list of past games to a json file
        :param data: list of past games
        :return: None
        """
        with open(self.config.JSON_PATH, "w") as file:
            json.dump(data, file)

    def create_result(self, result: str) -> Dict:
        """
        Create a dictionary with the result of the game in format as below:
        {
            "result": result of the game,
            "winner": winner of the game,
            "game_type": type of the game,
            "history": list of moves,
            "player_color": color of the player(null in PvP),
            "engine_elo": elo of the engine(null in PvP),
            "time_started": time the game started,
            "time_ended": time the game ended
        }
        :param result: result of the game
        :return: dictionary with the result of the game
        """
        return {
            "result": result,
            "winner": (
                ("white" if self.map.curr_player == "black" else "black")
                if result == "mate"
                else None
            ),
            "game_type": (
                "player vs computer"
                if self.game_type == "computer"
                else "player vs player"
            ),
            "history": self.map.history,
            "player_color": self.player_color if self.game_type == "computer" else None,
            "engine elo": self.elo if self.game_type == "computer" else None,
            "time started": self.game_time_start,
            "time ended": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def save_game(self, result: str) -> None:
        """
        Save the current game to the json file
        :param result: result of the game
        :return: None
        """
        if self.game_saved:
            return
        data = self.read_json()
        data.append(self.create_result(result))
        self.write_json(data)
        self.game_saved = True
        upload_new(data)  # uncomment this line to upload the game to the database

    def main(self) -> int:
        """
        Main function to run the game and handle the events
        :return: 1 if we choose to quit, 0 elsewhere
        """
        pygame.init()
        pygame.font.init()
        if self.handle_menu():
            pygame.quit()
            return 1

        timer = pygame.time.Clock()
        pygame.display.set_caption("Chess App")
        self.engine.set_position([])
        self.eval_engine.set_position([])
        evaluation = self.eval_engine.get_evaluation()

        self.game_time_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        while self.running:
            timer.tick(self.config.FPS)
            self.controller.update_screen(evaluation["value"])
            self.fps_counter += 1

            if (
                self.game_type == "computer"
                and self.map.curr_player == self.engine_color
                and not self.mate
                and not self.stalemate
                and not self.map.promoting_piece
            ):
                pygame.display.flip()  # might seem redundant but prevents user move lag
                result = self.engine.get_best_move()
                sleep(0.2)
                self.map.make_engine_move(result, self.player_color, self.engine_color)
                self.engine.make_moves_from_current_position([result])
                self.eval_engine.make_moves_from_current_position([result])
                self.map.check(self.map.curr_player)
                self.mate = self.map.calculate_mate()
                self.stalemate = self.map.calculate_stalemate()
                evaluation = self.eval_engine.get_evaluation()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if (
                    self.map.curr_player == self.player_color
                    or self.game_type == "onboard"
                ):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if self.new_game_button_clicked(x, y):
                            return 0

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
                                evaluation = self.eval_engine.get_evaluation()

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
                        self.eval_engine.make_moves_from_current_position([last_move])
                        self.map.promoting_piece = None
                        self.map.check(self.map.curr_player)
                        self.mate = self.map.calculate_mate()
                        self.stalemate = self.map.calculate_stalemate()
                        evaluation = self.eval_engine.get_evaluation()
            if self.mate:
                self.controller.draw_message(
                    "white" if self.map.curr_player == "black" else "black",
                    None,
                    self.game_type,
                    self.player_color,
                )
                self.save_game("mate")

            elif self.stalemate:
                self.controller.draw_message(None, "Stalemate", None, None)
                self.save_game("stalemate")

                # dragging piece
            if self.mouse_down and self.selected_piece:
                x, y = pygame.mouse.get_pos()
                self.controller.drag_piece(x, y, self.selected_piece)

            if self.mouse_down:
                self.controller.draw_possible_moves(self.moves, self.attack_moves)

            if self.map.check_white or self.map.check_black:
                self.controller.draw_checks()

            # if self.fps_counter % 100 == 0:
            #     print(self.map.history)

            pygame.display.flip()

        pygame.quit()

        return 0
