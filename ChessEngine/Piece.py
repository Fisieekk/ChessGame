from ChessEngine.Position import Position


class Piece:
    def __init__(self, y: int, x: int, color: str):
        self.position = Position(x=x, y=y)
        self.color = color
        self.has_moved = False
        self.picture = None
        self.last_move = None

    def get_picture(self) -> str:
        return self.picture

    def get_last_move(self) -> list:
        return self.last_move

    def move(self, position: Position) -> None:
        self.position = position
        self.has_moved = True

    def create_moves(self, map, output: list) -> tuple:
        moves = []
        attack_moves = []
        for move in output:
            new_position = Position(x=self.position.x + move[1], y=self.position.y + move[0])
            while new_position.in_board() and map.board[new_position.y][new_position.x] is None:
                moves.append([new_position.y, new_position.x])
                new_position.x += move[1]
                new_position.y += move[0]

            if 8 > new_position.x >= 0 and 8 > new_position.y >= 0 and map.board[new_position.y][
                new_position.x] is not None and \
                    map.board[new_position.y][new_position.x].color != self.color:
                attack_moves.append([new_position.y, new_position.x])

        return moves, attack_moves

    def get_identificator(self) -> str:
        pass
