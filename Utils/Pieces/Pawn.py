from Utils.Piece import Piece
class Pawn(Piece):
    def __init__(self, position,color):
        super().__init__(position)
        self.color= color
        self.type = "Pawn"
        self.photo="Images/wp.png" if color == "white" else "Images/bp.png"

    def can_move(self,board):
        # Ten ruch poprawie kiedy bede dodawał roszade
        output = []
        moves = []
        attack_moves = []
        new_y = self.y + 1
        if self.x<8 and self.x>0 and board.map[new_y][self.x] == None:
            moves.append([self.x,new_y])
            if self.last_move == None and board.map[new_y+1][self.x] == None:
                moves.append([self.x,new_y+1])
        new_y = self.y + 1
        for i in (-1,1):
            new_x = self.x + i
            if new_x<8 and new_x>=0 and board.map[new_y][new_x] and board.map[new_y][new_x].color != self.color:
                attack_moves.append([new_x,new_y])
                attack_moves.append([new_x,new_y])
        en_passant_moves = []
        for i in (-1, 1):
            if self.x + i >= 0 and self.x + i < 8 and self.y:
                possible_target = board.board_arr[self.x + i][self.y]
                if type(possible_target) == Pawn and self.color != possible_target.color:
                    last_move = board.last_move()
                    if last_move is not None and last_move[2] == self.symbol and last_move[4][0] == self.x + i \
                            and abs(last_move[4][1] - last_move[3][1]) == 2:
                        en_passant_moves.append([self.x + i, self.y])
        attack_moves+=en_passant_moves(board)
        return moves, attack_moves
    def get_type(self):
        return self.type

    def get_identificator(self):
        return self.color[0]+'P'

