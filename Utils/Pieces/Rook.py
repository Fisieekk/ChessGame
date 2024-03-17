from Utils.Piece import Piece
class Rook(Piece):
    def __init__(self, position,color):
        super().__init__(position)
        self.color= color
        self.type = "Rook"
        self.photo="images/wR.png" if color == "white" else "images/bR.png"

    def rook_can_moves(self,board):
        output = ((-1,0),(1,0),(0,-1),(0,1))
        return self.create_moves(board,output)

    def get_type(self):
        return self.type

    def get_identificator(self):
        return self.color[0]+'R'