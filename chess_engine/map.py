from typing import Optional

from .piece import Piece
from .position import Position
from .pieces import Bishop, King, Knight, Pawn, Queen, Rook


class Map:
    def __init__(self, width, height):
        """
        :param width: width of the board
        :param height: height of the board
        """
        self.curr_player = "white"
        self.history = []
        self.last_move = None
        self.turn = 1
        self.promoting_piece = None
        self.white_king_position = Position(x=4, y=7)
        self.black_king_position = Position(x=4, y=0)
        self.check_white = False
        self.check_black = False
        self.white_king_moved = False
        self.black_king_moved = False
        self.winner = None
        self.width = width
        self.height = height
        self.white_captured_value = 0
        self.black_captured_value = 0
        self.weights = {"P": 1, "B": 3, "N": 3, "R": 5, "Q": 9}
        self.board = [
            [
                Rook(0, 0, "black"),
                Knight(0, 1, "black"),
                Bishop(0, 2, "black"),
                Queen(0, 3, "black"),
                King(0, 4, "black"),
                Bishop(0, 5, "black"),
                Knight(0, 6, "black"),
                Rook(0, 7, "black"),
            ],
            [
                Pawn(1, 0, "black"),
                Pawn(1, 1, "black"),
                Pawn(1, 2, "black"),
                Pawn(1, 3, "black"),
                Pawn(1, 4, "black"),
                Pawn(1, 5, "black"),
                Pawn(1, 6, "black"),
                Pawn(1, 7, "black"),
            ],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [
                Pawn(6, 0, "white"),
                Pawn(6, 1, "white"),
                Pawn(6, 2, "white"),
                Pawn(6, 3, "white"),
                Pawn(6, 4, "white"),
                Pawn(6, 5, "white"),
                Pawn(6, 6, "white"),
                Pawn(6, 7, "white"),
            ],
            [
                Rook(7, 0, "white"),
                Knight(7, 1, "white"),
                Bishop(7, 2, "white"),
                Queen(7, 3, "white"),
                King(7, 4, "white"),
                Bishop(7, 5, "white"),
                Knight(7, 6, "white"),
                Rook(7, 7, "white"),
            ],
        ]

    def stalemate_test(self):
        """
        Method to simplify the stalemate test.
        :return: none
        """
        self.board = [
            [King(0, 0, "black"), None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [
                None,
                None,
                None,
                Queen(7, 3, "white"),
                King(7, 4, "white"),
                None,
                None,
                None,
            ],
        ]

    def move_to_uci(self, move: tuple[Position, Position]) -> str:
        """
        Method to convert move to UCI notation.
        :param move: move to be converted
        :return: UCI notation of the move
        """
        start, end = move
        return (
                chr(start.x + 97)
                + str(8 - start.y)
                + chr(end.x + 97)
                + str(8 - end.y)
        )

    def move(self, start: Position, end: Position) -> None:
        """
        Method to move a piece from start to end position.
        :param start: start position of piece
        :param end:  end position of piece
        :return None
        """
        piece, self.board[start.y][start.x] = self.board[start.y][start.x], None
        castle_uci = ""
        if type(piece) == King:
            # if Castle

            if piece.color == "white" and not self.white_king_moved:
                self.white_king_position = end
                if (end.y, end.x) == (7, 6):
                    self.board[7][7].move(Position(x=5, y=7))
                    self.board[7][5] = self.board[7][7]
                    self.board[7][7] = None
                    castle_uci = "e1g1"
                elif (end.y, end.x) == (7, 2):
                    self.board[7][0].move(Position(x=3, y=7))
                    self.board[7][3] = self.board[7][0]
                    self.board[7][0] = None
                    castle_uci = "e1c1"
            elif piece.color == "black" and not self.black_king_moved:
                self.black_king_position = end
                if (end.y, end.x) == (0, 6):
                    self.board[0][7].move(Position(x=5, y=0))
                    self.board[0][5] = self.board[0][7]
                    self.board[0][7] = None
                    castle_uci = "e8g8"
                elif (end.y, end.x) == (0, 2):
                    self.board[0][0].move(Position(x=3, y=0))
                    self.board[0][3] = self.board[0][0]
                    self.board[0][0] = None
                    castle_uci = "e8c8"
            if piece.color == "white":
                self.white_king_position = end
                self.white_king_moved = True
            if piece.color == "black":
                self.black_king_position = end
                self.black_king_moved = True
        piece.move(end)
        piece.last_move = self.turn
        self.board[end.y][end.x] = piece
        self.last_move = (start, end, piece)
        if type(piece) == Pawn and (end.y == 0 or end.y == 7):
            self.promoting_piece = piece
        self.history.append(self.move_to_uci((start, end)) if castle_uci == "" else castle_uci)
        self.turn += 1

    def en_passant_move(self, start: Position, end: Position) -> None:
        """
        Method to move a piece using en passant.
        :param start: start position of piece
        :param end: end position of piece
        :return None
        """
        self.board[start.y][end.x] = None
        self.move(start, end)

    def all_possible_attacks(self, color: str) -> list:
        """
        Method to get all possible attacks for a given color.
        :param color: color of the player
        :return: None
        """
        possible_attacks = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None and self.board[i][j].color == color:
                    moves, attack_moves = self.board[i][j].can_move(self)
                    possible_attacks += attack_moves
        return possible_attacks

    def all_possible_moves(self, color: str) -> list:
        """
        Method to get all possible moves for a given color.
        :param color: color of the player
        :return: list of possible moves
        """
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None and self.board[i][j].color == color:
                    moves, attack_moves = self.board[i][j].can_move(self)
                    moves, attack_moves = self.preventer(
                        moves, attack_moves, self.board[i][j]
                    )
                    possible_moves += attack_moves
                    possible_moves += moves
        return possible_moves

    def preventer(
            self, moves: list, attack_moves: list, piece: Piece
    ) -> tuple[list, list]:
        """
        Method to prevent a move that is illegal.
        :param moves: all moves of the piece
        :param attack_moves:  all attack moves of the piece
        :param piece: piece to prevent
        :return: lists of moves and attack moves
        """
        old_position = piece.position
        self.board[old_position.y][old_position.x] = None
        color = piece.color
        moves_to_remove = []
        for move in moves:
            new_position = move
            self.board[new_position.y][new_position.x] = piece
            if type(piece) == King:
                if color == "white":
                    self.white_king_position = new_position
                else:
                    self.black_king_position = new_position
            if color == "white":
                if self.white_king_position in self.all_possible_attacks("black"):
                    moves_to_remove.append(move)
            else:
                if self.black_king_position in self.all_possible_attacks("white"):
                    moves_to_remove.append(move)
            self.board[new_position.y][new_position.x] = None
            if type(piece) == King:
                if color == "white":
                    self.white_king_position = old_position
                else:
                    self.black_king_position = old_position
        for move in attack_moves:
            new_position = move
            temp, self.board[new_position.y][new_position.x] = (
                self.board[new_position.y][new_position.x],
                piece,
            )
            if type(piece) == King:
                if color == "white":
                    self.white_king_position = new_position
                else:
                    self.black_king_position = new_position
            if color == "white":
                if self.white_king_position in self.all_possible_attacks("black"):
                    moves_to_remove.append(move)
            else:
                if self.black_king_position in self.all_possible_attacks("white"):
                    moves_to_remove.append(move)
            self.board[new_position.y][new_position.x] = temp
            self.board[old_position.y][old_position.x] = piece
            if type(piece) == King:
                if color == "white":
                    self.white_king_position = old_position
                else:
                    self.black_king_position = old_position
        for move in moves_to_remove:
            if move in moves:
                moves.remove(move)
            elif move in attack_moves:
                attack_moves.remove(move)
        self.board[old_position.y][old_position.x] = piece
        return moves, attack_moves

    def check(self, color: str) -> None:
        """
        Method to check if a player is in check.
        :param color: color of the player
        :return: None
        """
        """
        print(color)
        print(self.all_possible_attacks("white"))
        print(self.black_king_position)
        """

        if color == "white" and self.white_king_position in self.all_possible_attacks(
                "black"
        ):
            self.check_white = True
            self.check_black = False
        elif color == "black" and self.black_king_position in self.all_possible_attacks(
                "white"
        ):
            self.check_white = False
            self.check_black = True
        else:
            self.check_white = False
            self.check_black = False

    def castle(
            self, moves: list, attack_moves: list, piece: Piece
    ) -> tuple[list, list]:
        """
        Method to add a castle to possible moves.
        :param moves: possible moves of piece
        :param attack_moves: possible attack moves of piece
        :param piece: to castle
        :return: lists of moves and attack moves
        """
        if piece.last_move is not None:
            return moves, attack_moves
        if piece.color == "white":
            if self.board[7][7] is not None:
                if self.board[7][7].last_move is None:
                    if self.board[7][6] is None and self.board[7][5] is None:
                        moves.append(Position(x=6, y=7))
            if self.board[7][0] is not None:
                if self.board[7][0].last_move is None:
                    if (
                            self.board[7][1] is None
                            and self.board[7][2] is None
                            and self.board[7][3] is None
                    ):
                        moves.append(Position(x=2, y=7))
        else:
            if self.board[0][7] is not None:
                if self.board[0][7].last_move is None:
                    if self.board[0][6] is None and self.board[0][5] is None:
                        moves.append(Position(x=6, y=0))
            if self.board[0][0] is not None:
                if self.board[0][0].last_move is None:
                    if (
                            self.board[0][1] is None
                            and self.board[0][2] is None
                            and self.board[0][3] is None
                    ):
                        moves.append(Position(x=2, y=0))

        return moves, attack_moves

    def calculate_mate(self) -> bool:
        """
        Method to calculate if a player is in mate.
        :return: bool value True if player is in mate else False
        """
        if not self.check_white and not self.check_black:
            return False
        friendly_moves = self.all_possible_moves(self.curr_player)
        if len(friendly_moves) == 0:
            return True
        return False

    def calculate_stalemate(self) -> bool:
        """
        Method to calculate if there is a stalemate.
        :return: bool value True if there is a stalemate else False
        """
        if self.check_white or self.check_black:
            return False
        if len(self.all_possible_moves(self.curr_player)) == 0:
            return True
        return False

    def evaluate_captured_piece(self, captured_piece: Piece) -> None:
        """
        Method to evaluate the captured piece.
        :param captured_piece: piece that has been captured
        :return: None
        """
        if captured_piece.get_identificator()[-1] == "K":
            return
        if captured_piece.color == "white":
            self.black_captured_value += self.weights[
                captured_piece.get_identificator()[1]
            ]
        else:
            self.white_captured_value += self.weights[
                captured_piece.get_identificator()[1]
            ]

    def change_piece(self, position: Optional[Position], identifier: str) -> None:
        """
        Method to change a piece after promotion.
        :param position: position of the piece to be changed
        :param identifier: identifier of the piece to be placed on the board
        :return: None
        """
        color = "white" if identifier[0] == "w" else "black"
        if position is None:
            position = self.promoting_piece.position
        row, col = position.y, position.x
        if identifier[1] == "Q":
            self.board[row][col] = Queen(row, col, color)
            self.history[-1] += identifier[1].lower()
        elif identifier[1] == "N":
            self.board[row][col] = Knight(row, col, color)
            self.history[-1] += identifier[1].lower()
        elif identifier[1] == "R":
            self.board[row][col] = Rook(row, col, color)
            self.history[-1] += identifier[1].lower()
        else:
            self.board[row][col] = Bishop(row, col, color)
            self.history[-1] += identifier[1].lower()

        self.promoting_piece = None

    def make_engine_move(self, move: str) -> None:
        """
        Method to make a move for the engine.
        For now engine will be playing only as black.
        :param move: move to be made
        :return: None
        """
        start = Position(x=ord(move[0]) - 97, y=8 - int(move[1]))
        end = Position(x=ord(move[2]) - 97, y=8 - int(move[3]))
        self.move(start, end)
        if len(move) == 5:
            self.change_piece(end, 'b' + move[4].upper())
            self.history[-1] += move[4].lower()
        self.curr_player = "white"

    def get_eight_last_moves(self) -> tuple[list, list, int]:
        """
        Method to get the last eight moves.
        :return: tuple of two lists of moves and the number of moves
        """
        black_moves = []
        white_moves = []
        moves_number = len(self.history) // 2
        for i in range(len(self.history) - 1, -1, -1):
            if i % 2 == 0:
                black_moves.append(self.history[i])
            else:
                white_moves.append(self.history[i])
            if len(black_moves) == 8 and len(white_moves) == 8:
                break
        return white_moves, black_moves, moves_number
