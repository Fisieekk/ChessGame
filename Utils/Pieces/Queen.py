from Utils.Piece import Piece
class Queen(Piece):
    def __init__(self, position,color):
        super().__init__(position)
        self.color= color
        self.type = "Queen"
        self.photo="Tutaj ścieżka do Hetmana"

    def queen_can_move(self,board):
        moves,attack_moves=self.rook_can_moves(board)
        #moves,attack_moves+=self.bishop_can_moves(board)
        return moves,attack_moves

    def get_type(self):
        return self.type

    def get_identificator(self):
        return self.color[0]+'R'
