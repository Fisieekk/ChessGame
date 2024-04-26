from Utils.Piece import Piece
class Pawn(Piece):
    def __init__(self, position,color):
        super().__init__(position)
        self.color= color
        self.type = "Pawn"
        self.photo="Images/wp.png" if color == "white" else "Images/bp.png"

    def can_move(self,board):
        if self.color=="white":
            poss_change=-1
        else:
            poss_change=1
        moves = []
        attack_moves = []
        new_y = self.y + poss_change
        if self.x<8 and self.x>=0 and new_y<8 and new_y>=0 and board.board[new_y][self.x] == None:
            moves.append([new_y,self.x])
            if self.last_move == None:
                new_y += poss_change
                if board.board[new_y][self.x] == None:
                    moves.append([new_y,self.x])
        new_y = self.y + poss_change
        en_passant_moves = []
        for i in (-1,1):
            new_x = self.x + i
            if new_x<8 and new_x>=0 and new_y>=0 and new_y<8 and board.board[new_y][new_x] and board.board[new_y][new_x].color != self.color:
                attack_moves.append([new_y,new_x])
            if (board.last_move):
                if new_x<8 and new_x>=0 and self.y == board.last_move[1][0] and new_y == board.last_move[1][0]+poss_change and new_x == board.last_move[1][1] and type(board.last_move[2])==Pawn:
                    en_passant_moves.append([new_y,new_x])
        attack_moves += en_passant_moves
        return moves, attack_moves
    def get_type(self):
        return self.type

    def get_identificator(self):
        return self.color[0]+'P'



