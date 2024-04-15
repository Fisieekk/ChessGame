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
        self.history = []
        self.last_move = None
        self.turn = 1
        self.promotion = None
        self.white_king_position = [7, 4]
        self.black_king_position = [0, 4]
        self.check_white = False
        self.check_black = False
        self.white_king_moved = False
        self.black_king_moved = False
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

    def move(self, start, end):
        piece, self.board[start[0]][start[1]] = self.board[start[0]][start[1]], None
        if type(piece) == King:
            if piece.color == "white" and not self.white_king_moved:
                self.white_king_position = [end[0], end[1]]
                if end == (7, 6):
                    self.board[7][7].move((7, 5))
                    self.board[7][5] = self.board[7][7]
                    self.board[7][7] = None
                elif end == (7, 2):
                    self.board[7][0].move((7, 3))
                    self.board[7][3] = self.board[7][0]
                    self.board[7][0] = None

            elif piece.color == "black" and not self.black_king_moved:
                self.black_king_position = [end[0], end[1]]
                if end == (0, 6):
                    self.board[0][7].move((0, 5))
                    self.board[0][5] = self.board[0][7]
                    self.board[0][7] = None
                elif end == (0, 2):
                    self.board[0][0].move((0, 3))
                    self.board[0][3] = self.board[0][0]
                    self.board[0][0] = None
            if piece.color== 'white':
                self.white_king_moved = True
            if piece.color=='black':
                self.black_king_moved = True
        piece.move(end)
        piece.last_move = self.turn
        self.board[end[0]][end[1]] = piece
        self.history.append((piece, self.turn, piece.color, piece.type, start, end))
        self.last_move = (start, end)
        if type(piece) == Pawn and (end[0] == 0 or end[0] == 7):
            self.promotion = piece
            promotionn(self, piece, end)
        self.turn += 1

    def all_possible_attacks(self, color):
        possible_attacks = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None and self.board[i][j].color == color:
                    moves, attack_moves = self.board[i][j].can_move(self)
                    possible_attacks += attack_moves
        return possible_attacks

    def preventer(self, moves, attack_moves, piece):
        old_y, old_x = piece.position
        self.board[old_y][old_x] = None
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
                    self.check_white = True
            elif self.black_king_position in self.all_possible_attacks("white"):
                moves_to_remove.append(move)
                self.check_black = True
            else:
                self.check_white = False
                self.check_black = False
            self.board[new_y][new_x] = None
            if type(piece) == King:
                if color == "white":
                    self.white_king_position = [old_y, old_x]
                else:
                    self.black_king_position = [old_y, old_x]
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
            self.board[old_y][old_x] = piece
            if type(piece) == King:
                if color == "white":
                    self.white_king_position = [old_y, old_x]
                else:
                    self.black_king_position = [old_y, old_x]
        for move in moves_to_remove:
            if move in moves:
                moves.remove(move)
        self.board[old_y][old_x] = piece
        return moves, attack_moves

    def castle(self, moves, attack_moves, piece):
        if piece.last_move is not None:
            return moves, attack_moves
        if piece.color == "white":
            if self.board[7][7].last_move is None:
                if self.board[7][6] is None and self.board[7][5] is None:
                    moves.append((7, 6))
            if self.board[7][0].last_move is None:
                if self.board[7][1] is None and self.board[7][2] is None and self.board[7][3] is None:
                    moves.append((7, 2))
        else:
            if self.board[0][7].last_move is None:
                if self.board[0][6] is None and self.board[0][5] is None:
                    moves.append((0, 6))
            if self.board[0][0].last_move is None:
                if self.board[0][1] is None and self.board[0][2] is None and self.board[0][3] is None:
                    moves.append((0, 2))

        return moves, attack_moves


def promotionn(self, piece, position):
    # placeholder
    print("promotion")
    pass

    # def preventer(self,start,end):
    #     old_y,old_x=start
    #     new_y,new_x=end
    #     piece,self.board[old_y][old_x]=self.board[old_y][old_x],None
    #     color=piece.color
    #     if color=="white":
    #         if self.white_king_position in self.all_possible_attacks("black"):
    #             self.board[old_y][old_x]=piece
    #             return False
    #     else:
    #         if self.black_king_position in self.all_possible_attacks("white"):
    #             self.board[old_y][old_x]=piece
    #             return False
    #     self.board[old_y][old_x]=piece
    #     return True

    # def piece_moves(self, start, end):
    #     moves, attack_moves = start.can_move(self)

    # def last_move(self):
    #     return None if not self.moves else self.moves[-1]

    # def get_possible_attacks(self, color):
    #     possible_attacks = []
    #     for i in range(8):
    #         for j in range(8):
    #             if self.board[i][j] is not None and self.board[i][j].color == color:
    #                 moves, attack_moves = self.board[i][j].can_move(self)
    #                 possible_attacks += attack_moves
    #     return possible_attacks

    # def try_move(self, start, end):
    #     old_x = start[1]
    #     old_y = start[0]
    #     new_x = end[1]
    #     new_y = end[0]
    #     piece = self.board[old_y][old_x]
    #     attacked_piece = self.board[new_y][new_x]
    #     all_enemy_attacks = self.get_possible_attacks(piece.color)
    #     self.board[old_y][old_x], self.board[new_y][new_x] = None, self.board[old_y][old_x]
    #     piece.move(end)

    #     for capture_position in all_enemy_attacks:
    #         another_piece = self.board[capture_position[0]][capture_position[1]]
    #         if (type(another_piece)==King and another_piece.color==piece.color):
    #             self.block_move(piece, attacked_piece, start, end)

    #             return False

    #     self.block_move(piece, attacked_piece, start, end)
    #     return True

    # def block_move(self, piece, attacked_piece, start, end):
    #     self.board[start[0]][start[1]] = piece
    #     self.board[end[0]][end[1]] = attacked_piece
    #     piece.move(start)

    # def move(self, start, end):
    #     piece, self.board[start[0]][start[1]] = self.board[start[0]][start[1]], None
    #     old_x, old_y = start
    #     print(piece.position)
    #     piece.move(end)
    #     print(piece.position)
    #     piece.last_move = self.turn
    #     self.board[end[0]][end[1]] = piece
    #     self.moves.append((piece, self.turn, piece.color, piece.type, start, end))
    #     self.turn += 1
    #     self.check_black = False
    #     self.check_white = False
    #     self.check()

    # def checkmate(self):
    #     for i in range(8):
    #         for j in range(8):
    #             if self.board[i][j] != None and self.board[i][j].color == self.curr_player:
    #                 moves, attack_moves = self.board[i][j].can_move(self)
    #                 for move in moves:
    #                     if self.try_move((i, j), move):
    #                         return False
    #     self.check()
    #     if self.check_white:
    #         self.winner = 'black'
    #     elif self.check_black:
    #         self.winner = 'white'
    #     else:
    #         self.winner = 'draw'
    #     return True

    # def check(self):
    #     for i in range(8):
    #         for j in range(8):
    #             if self.board[i][j] != None and self.board[i][j].color != self.curr_player:
    #                 moves, attack_moves = self.board[i][j].can_move(self)
    #                 for move in attack_moves:
    #                     if type(self.board[move[1]][move[0]]) == King:
    #                         if self.board[move[1]][move[0]].color == 'white':
    #                             self.check_white = True
    #                         else:
    #                             self.check_black = True
    #                         return
