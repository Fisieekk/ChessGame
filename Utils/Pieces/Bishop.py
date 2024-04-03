from Utils.Piece import Piece


class Bishop(Piece):
    def __init__(self, position, color):
        super().__init__(position)
        self.color = color
        self.type = "Bishop"
        self.photo = "images/wB.png" if color == "white" else "images/bB.png"

    def can_move(self, board):
        print(self.position)
        return self.bishop_moves(board)

    def bishop_moves(self,board):
        output = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        print(self.create_moves(board,output))
        return self.create_moves(board,output)


    def get_type(self):
        return self.type

    def get_identificator(self):
        return self.color[0] + 'B'
