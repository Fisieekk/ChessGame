from Utils.Piece import Piece
class Knight(Piece):
    def __init__(self, position,color):
        super().__init__(position)
        self.color= color
        self.type = "Knight"
        self.photo="Images/wN.png" if color == "white" else "Images/bN.png"

    def can_move(self,board):
        moves = []
        attack_moves = []
        moves_comb=[-2,-1,1,2]
        for i in moves_comb:
            for j in moves_comb:
                new_x = self.x + i
                new_y = self.y + j
                if abs(i) != abs(j) and new_x >= 0 and new_x < 8 and new_y >= 0 and new_y < 8:
                    if board.board[new_y][new_x] is None:
                        moves.append([new_y, new_x])
                    else:
                        if board.board[new_y][new_x].color != self.color:
                            attack_moves.append([new_y, new_x])
        return moves,attack_moves
    def get_type(self):
        return self.type

    def get_identificator(self):
        return self.color[0]+'N'

