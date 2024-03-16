from Utils.Piece import Piece
class King(Piece):
    def __init__(self, position,color):
        super().__init__(position)
        self.color= color
        self.type = "King"
        self.photo="Tutaj ścieżka do Króla"

    def can_move(self,board):
        moves = []
        attack_moves = []
        castle_moves = self.castle(board.map)

        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                new_x = self.x + i
                new_y = self.y + j
                if (i != 0 or j != 0) and new_x >= 0 and new_x < 8 and new_y >= 0 and new_y < 8:
                    if board.map[new_x][new_y] is None:
                        moves.append([new_x, new_y])
                    else:
                        if board.map[new_x][new_y].color != self.color:
                            attack_moves.append([new_x, new_y])

        moves += castle_moves
        return moves, attack_moves
    def castle(self,map):
        castle_moves = []
        left_rook = map[0][self.y]
        right_rook = map[7][self.y]
        #Trzeba dodać can_castle do mapy ale teraz nie mam siły
        if self.last_move is None:
            if can_castle(left_rook) and (map[1][self.y] is None and map[2][self.y] is None and map[3][self.y] is None):
                castle_moves.append([2, self.y])
            if can_castle(right_rook) and (map[5][self.y] is None and map[6][self.y] is None):
                castle_moves.append([6, self.y])

        return castle_moves
    def get_type(self):
        return self.type

    def get_identificator(self):
        return self.color[0]+'K'