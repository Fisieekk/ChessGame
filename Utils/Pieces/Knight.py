from Utils.Piece import Piece
class Knight(Piece):
    def __init__(self, position,color):
        super().__init__(position)
        self.color= color
        self.type = "Knight"
        self.photo="Tutaj ścieżka do Skoczka"

    def can_move(self,board):
        moves = []
        attack_moves = []

        for i in (-2, -1, 1, 2):
            for j in (-2, -1, 1, 2):
                new_x = self.x + i
                new_y = self.y + j
                if abs(i) != abs(j) and new_x >= 0 and new_x < 8 and new_y >= 0 and new_y < 8:
                    if board.board_arr[new_x][new_y] is None:
                        moves.append([new_x, new_y])
                    else:
                        if board.board_arr[new_x][new_y].color != self.color:
                            attack_moves.append([new_x, new_y])
    def get_type(self):
        return self.type

    def get_identificator(self):
        return self.color[0]+'N'
