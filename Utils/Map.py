from .Pieces.Bishop import Bishop
from .Pieces.King import King
from .Pieces.Knight import Knight
from .Pieces.Pawn import Pawn
from .Pieces.Queen import Queen
from .Pieces.Rook import Rook
from .Piece import Piece


class Map:
    # Trzeba dodać zmienną przechowującą ostatni ruch. Potrzebna do en passant
    def __init__(self, width, height):
        self.curr_player = 'white'
        self.moves = []
        self.turn = 1
        self.promotion = None
        self.check_white = False
        self.check_black = False
        self.winner = None
        self.width = width
        self.height = height
        self.board = [
            [Rook((0, 0), 'black'), Knight((0, 1), 'black'), Bishop((0, 2), 'black'), Queen((0, 3), 'black'),
             King((0, 4), 'black'), Bishop((0, 5), 'black'), Knight((0, 6), 'black'), Rook((0, 7), 'black')],
            [Pawn((1, 0), 'black'), Pawn((1, 1), 'black'), Pawn((1, 2), 'black'), Pawn((1, 3), 'black'),
             Pawn((1, 4), 'black'), Pawn((1, 5), 'black'), Pawn((1, 6), 'black'), Pawn((1, 7), 'black')],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn((6, 0), 'white'), Pawn((6, 1), 'white'), Pawn((6, 2), 'white'), Pawn((6, 3), 'white'),
             Pawn((6, 4), 'white'), Pawn((6, 5), 'white'), Pawn((6, 6), 'white'), Pawn((6, 7), 'white')],
            [Rook((7, 0), 'white'), Knight((7, 1), 'white'), Bishop((7, 2), 'white'), Queen((7, 3), 'white'),
             King((7, 4), 'white'), Bishop((7, 5), 'white'), Knight((7, 6), 'white'), Rook((7, 7), 'white')]
        ]

    def piece_moves(self, start, end):
        moves, attack_moves = start.can_move(self)
        print(moves)
    
    def last_move(self):
        return None if not self.moves else self.moves[-1]

    def get_possible_attacks(self, color):
        possible_attacks = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None and self.board[i][j].color == color:
                    moves, attack_moves = self.board[i][j].can_move(self)
                    possible_attacks += attack_moves
        return possible_attacks

    def try_move(self, start, end):
        old_x = start[0]
        old_y = start[1]
        new_x = end[0]
        new_y = end[1]
        piece = self.board[old_x][old_y]
        attacked_piece = self.board[new_x][new_y]
        all_enemy_attacks = self.get_possible_attacks(piece.color)
        self.board[old_x][old_y], self.board[new_x][new_y] = None, self.board[old_x][old_y]
        piece.move(end)

        for capture_position in all_enemy_attacks:
            if (self.white_king.get_position() == capture_position and piece.color == 'w') \
                    or (self.black_king.get_position() == capture_position and piece.color == 'b'):
                self.block_move(piece, attacked_piece, start, end)

                return False

        self.block_move(piece, attacked_piece, start, end)
        return True

    def block_move(self, piece, attacked_piece, start, end):
        self.board_arr[start[0]][start[1]] = piece
        self.board_arr[end[0]][end[1]] = attacked_piece
        piece.move(start)

    def move(self, start, end):
        piece, self.board[start[0]][start[1]] = self.board[start[0]][start[1]], None
        old_x, old_y = start
        piece.move(end)
        piece.last_move = self.turn
        self.board[end[0]][end[1]] = piece
        self.moves.append((piece, self.turn, piece.color, piece.type, start, end))
        self.turn += 1
        self.check_black = False
        self.check_white = False
        self.check()

    def checkmate(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != None and self.board[i][j].color == self.curr_player:
                    moves, attack_moves = self.board[i][j].can_move(self)
                    for move in moves:
                        if self.try_move((i, j), move):
                            return False
        self.check()
        if self.check_white:
            self.winner = 'black'
        elif self.check_black:
            self.winner = 'white'
        else:
            self.winner = 'draw'
        return True

    def check(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != None and self.board[i][j].color != self.curr_player:
                    moves, attack_moves = self.board[i][j].can_move(self)
                    for move in attack_moves:
                        if self.board[move[1]][move[0]].type == 'King':
                            if self.board[move[1]][move[0]].color == 'white':
                                self.check_white = True
                            else:
                                self.check_black = True
                            return

