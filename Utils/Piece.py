class Piece:
    def __init__(self, position):
        self.position = position
        self.y, self.x = position
        self.has_moved = False
        self.picture = None
        self.last_move = None

    # Getters
    def get_position(self):
        return self.position

    def get_picture(self):
        return self.picture
    def get_last_move(self):
        return self.last_move
    
    def set_position(self, x, y):
        self.position = (y, x)
        self.x = x
        self.y = y
    def move(self, new_position):
        self.set_position(new_position[1], new_position[0])
        self.has_moved = True

    def create_moves(self, board, output):
        moves = []
        attack_moves = []
        y,x = self.position
        for move in output:
            new_x = x + move[1]
            new_y = y + move[0]
            while 8 > new_x >= 0 and 8 > new_y >= 0 and board.board[new_y][new_x] is None:
                moves.append([new_y, new_x])
                new_x += move[1]
                new_y += move[0]

            if 8 > new_x >= 0 and 8 > new_y >= 0 and board.board[new_y][new_x] is not None and \
                    board.board[new_y][new_x].color != self.color:
                attack_moves.append([new_y, new_x])

        return moves, attack_moves
