from Utils.Piece import Piece
from .Bishop import Bishop
from .Rook import Rook
class Queen(Piece):
    def __init__(self, position,color):
        super().__init__(position)
        self.color= color
        self.type = "Queen"
        self.photo="Images/wQ.png" if color == "white" else "Images/bQ.png"

    def can_move(self,board):
        bishop = Bishop(self.position,self.color)
        rook = Rook(self.position,self.color)
        moves,attack_moves=rook.can_move(board)
        moves+=bishop.can_move(board)[0]
        attack_moves+=bishop.can_move(board)[1]
        return moves,attack_moves

    def get_type(self):
        return self.type

    def get_identificator(self):
        return self.color[0]+'Q'


