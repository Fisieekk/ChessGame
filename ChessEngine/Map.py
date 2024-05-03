from .Piece import Piece
from .Pieces.Bishop import Bishop
from .Pieces.King import King
from .Pieces.Knight import Knight
from .Pieces.Pawn import Pawn
from .Pieces.Queen import Queen
from .Pieces.Rook import Rook
from .Position import Position


class Map:
    def __init__(self, width, height):
        self.curr_player = 'white'
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
        self.weights = {'P': 1, 'B': 3, 'N': 3, 'R': 5, 'Q': 9}
        print(Rook)
        self.board = [
            [Rook(0, 0, 'black'), Knight(0, 1, 'black'), Bishop(0, 2, 'black'), Queen(0, 3, 'black'),
             King(0, 4, 'black'), Bishop(0, 5, 'black'), Knight(0, 6, 'black'), Rook(0, 7, 'black')],
            [Pawn(1, 0, 'black'), Pawn(1, 1, 'black'), Pawn(1, 2, 'black'), Pawn(1, 3, 'black'),
             Pawn(1, 4, 'black'), Pawn(1, 5, 'black'), Pawn(1, 6, 'black'), Pawn(1, 7, 'black')],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn(6, 0, 'white'), Pawn(6, 1, 'white'), Pawn(6, 2, 'white'), Pawn(6, 3, 'white'),
             Pawn(6, 4, 'white'), Pawn(6, 5, 'white'), Pawn(6, 6, 'white'), Pawn(6, 7, 'white')],
            [Rook(7, 0, 'white'), Knight(7, 1, 'white'), Bishop(7, 2, 'white'), Queen(7, 3, 'white'),
             King(7, 4, 'white'), Bishop(7, 5, 'white'), Knight(7, 6, 'white'), Rook(7, 7, 'white')]
        ]

    def stalemate_test(self):
        self.board = [
            [King(0, 0, 'black'), None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, Queen(7, 3, 'white'),
             King(7, 4, 'white'), None, None, None]
        ]

    def move(self, start: Position, end: Position) -> None:
        piece, self.board[start.y][start.x] = self.board[start.y][start.x], None
        if type(piece) == King:
            if piece.color == "white" and not self.white_king_moved:
                self.white_king_position = end
                if (end.y, end.x) == (7, 6):
                    self.board[7][7].move(7, 5)
                    self.board[7][5] = self.board[7][7]
                    self.board[7][7] = None
                elif (end.y, end.x) == (7, 2):
                    self.board[7][0].move(7, 3)
                    self.board[7][3] = self.board[7][0]
                    self.board[7][0] = None

            elif piece.color == "black" and not self.black_king_moved:
                self.black_king_position = [end.y, end.x]
                if end == (0, 6):
                    self.board[0][7].move(Position(x=5, y=0))
                    self.board[0][5] = self.board[0][7]
                    self.board[0][7] = None
                elif end == (0, 2):
                    self.board[0][0].move(Position(x=3, y=0))
                    self.board[0][3] = self.board[0][0]
                    self.board[0][0] = None
            if piece.color == 'white':
                self.white_king_moved = True
            if piece.color == 'black':
                self.black_king_moved = True
        piece.move(end)
        piece.last_move = self.turn
        self.board[end.y][end.x] = piece
        self.history.append((piece, self.turn, piece.color, piece.type, (start.y, start.x), (end.y, end.x)))
        self.last_move = (start, end, piece)
        if type(piece) == Pawn and (end.y == 0 or end.y == 7):
            self.promoting_piece = piece
        self.turn += 1

    def en_passant_move(self, start: Position, end: Position) -> None:
        print("en passant")
        self.board[start.y][end.x] = None
        self.move(start, end)

    def all_possible_attacks(self, color: str) -> list:
        possible_attacks = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None and self.board[i][j].color == color:
                    moves, attack_moves = self.board[i][j].can_move(self)
                    possible_attacks += attack_moves
        return possible_attacks

    def all_possible_moves(self, color: str) -> list:
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None and self.board[i][j].color == color:
                    moves, attack_moves = self.board[i][j].can_move(self)
                    moves, attack_moves = self.preventer(moves, attack_moves, self.board[i][j])
                    possible_moves += attack_moves
                    possible_moves += moves
        return possible_moves

    def preventer(self, moves: list, attack_moves: list, piece: Piece) -> tuple[list, list]:
        old_position = piece.position
        self.board[old_position.y][old_position.x] = None
        color = piece.color
        moves_to_remove = []
        for move in moves:
            new_y, new_x = move
            self.board[new_y][new_x] = piece
            if type(piece) == King:
                if color == "white":
                    self.white_king_position = [new_y, new_x]
                else:
                    self.black_king_position = [new_y, new_x]
            if color == "white":
                if self.white_king_position in self.all_possible_attacks("black"):
                    moves_to_remove.append(move)
            else:
                if self.black_king_position in self.all_possible_attacks("white"):
                    moves_to_remove.append(move)
            self.board[new_y][new_x] = None
            if type(piece) == King:
                if color == "white":
                    self.white_king_position = [old_position.y, old_position.x]
                else:
                    self.black_king_position = [old_position.y, old_position.x]
        for move in attack_moves:
            new_y, new_x = move
            temp, self.board[new_y][new_x] = self.board[new_y][new_x], piece
            if type(piece) == King:
                if color == "white":
                    self.white_king_position = [new_y, new_x]
                else:
                    self.black_king_position = [new_y, new_x]
            if color == "white":
                if self.white_king_position in self.all_possible_attacks("black"):
                    moves_to_remove.append(move)
            else:
                if self.black_king_position in self.all_possible_attacks("white"):
                    moves_to_remove.append(move)
            self.board[new_y][new_x] = temp
            self.board[old_position.y][old_position.x] = piece
            if type(piece) == King:
                if color == "white":
                    self.white_king_position = [old_position.y, old_position.x]
                else:
                    self.black_king_position = [old_position.y, old_position.x]
        for move in moves_to_remove:
            if move in moves:
                moves.remove(move)
            elif move in attack_moves:
                attack_moves.remove(move)
        self.board[old_position.y][old_position.x] = piece
        return moves, attack_moves

    def check(self, color: str) -> None:
        if color == "white" and self.white_king_position in self.all_possible_attacks("black"):
            self.check_white = True
            self.check_black = False
        elif color == 'black' and self.black_king_position in self.all_possible_attacks("white"):
            self.check_white = False
            self.check_black = True
        else:
            self.check_white = False
            self.check_black = False

    def castle(self, moves: list, attack_moves: list, piece: Piece) -> tuple[list, list]:
        if piece.last_move is not None:
            return moves, attack_moves
        if piece.color == "white":
            if self.board[7][7] is not None:
                if self.board[7][7].last_move is None:
                    if self.board[7][6] is None and self.board[7][5] is None:
                        moves.append((7, 6))
            if self.board[7][0] is not None:
                if self.board[7][0].last_move is None:
                    if self.board[7][1] is None and self.board[7][2] is None and self.board[7][3] is None:
                        moves.append((7, 2))
        else:
            if self.board[0][7] is not None:
                if self.board[0][7].last_move is None:
                    if self.board[0][6] is None and self.board[0][5] is None:
                        moves.append((0, 6))
            if self.board[0][0] is not None:
                if self.board[0][0].last_move is None:
                    if self.board[0][1] is None and self.board[0][2] is None and self.board[0][3] is None:
                        moves.append((0, 2))

        return moves, attack_moves

    def calculate_mate(self) -> bool:
        if not self.check_white and not self.check_black:
            return False
        friendly_moves = self.all_possible_moves(self.curr_player)
        if len(friendly_moves) == 0:
            return True
        return False

    def calculate_stalemate(self) -> bool:
        if self.check_white or self.check_black:
            return False
        if len(self.all_possible_moves(self.curr_player)) == 0:
            return True
        return False

    def evaluate_captured_piece(self, captured_piece: Piece) -> None:
        if captured_piece.get_identificator()[-1] == 'K':
            return
        if captured_piece.color == 'white':
            self.black_captured_value += self.weights[captured_piece.get_identificator()[1]]
        else:
            self.white_captured_value += self.weights[captured_piece.get_identificator()[1]]

    def change_piece(self, identifier: str) -> None:
        color = 'white' if identifier[0] == 'w' else 'black'
        position = self.promoting_piece.position
        row, col = position.y, position.x
        if identifier[1] == 'Q':
            self.board[row][col] = Queen(row, col, color)
        elif identifier[1] == 'N':
            self.board[row][col] = Knight(row, col, color)
        elif identifier[1] == 'R':
            self.board[row][col] = Rook(row, col, color)
        else:
            self.board[row][col] = Bishop(row, col, color)

        self.promoting_piece = None
