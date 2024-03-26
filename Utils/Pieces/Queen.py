from Utils.Piece import Piece
class Queen(Piece):
    def __init__(self, position,color):
        super().__init__(position)
        self.color= color
        self.type = "Queen"
        self.photo="Images/wQ.png" if color == "white" else "Images/bQ.png"

    def can_move(self,board):
        moves,attack_moves=self.rook_can_moves(board)
        moves+=self.bishop_can_moves(board)[0]
        attack_moves+=self.bishop_can_moves(board)[1]
        return moves,attack_moves

    def get_type(self):
        return self.type

    def get_identificator(self):
        return self.color[0]+'R'
