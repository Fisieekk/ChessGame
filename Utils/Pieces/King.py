from Utils.Piece import Piece
class King(Piece):
    def __init__(self, position,color):
        super().__init__(position)
        self.color= color
        self.type = "King"
        self.photo="images/wK.png" if color == "white" else "images/bK.png"

    def can_move(self,board):
        moves = []
        attack_moves = []
        castle_moves = self.castle(board)

        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                new_x = self.x + i
                new_y = self.y + j
                if (i != 0 or j != 0) and new_x >= 0 and new_x < 8 and new_y >= 0 and new_y < 8:
                    if board.board[new_y][new_x] is None:
                        moves.append([new_y,new_x])
                    else:
                        if board.board[new_y][new_x].color != self.color:
                            attack_moves.append([new_y ,new_x])

        moves += castle_moves
        return moves, attack_moves
    def can_castle(self,rook):
        return rook is not None and rook.type == "Rook" and not rook.has_moved
    def castle(self,board):
        castle_moves = []
        left_rook = board.board[self.y][0]
        right_rook = board.board[self.y][7]
        #Trzeba dodać can_castle do mapy ale teraz nie mam siły
        if self.last_move is None:
            if self.can_castle(left_rook) and (board.board[self.y][1] is None and board.board[self.y][2] is None and board.board[self.y][3] is None):
                castle_moves.append([self.y, 2])
            if self.can_castle(right_rook) and (board.board[self.y][5] is None and board.board[self.y][6] is None):
                castle_moves.append([self.y,6])

        return castle_moves
    def get_type(self):
        return self.type

    def get_identificator(self):
        return self.color[0]+'K'