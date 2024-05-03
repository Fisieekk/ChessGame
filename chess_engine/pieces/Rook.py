from chess_engine.Piece import Piece


class Rook(Piece):
    def __init__(self, y: int, x: int, color: str):
        super().__init__(y, x, color)
        self.type = "Rook"
        self.photo = "images/wR.png" if color == "white" else "images/bR.png"

    def can_move(self, map) -> tuple:
        return self.rook_moves(map)

    def rook_moves(self, board) -> tuple:
        output = ((-1, 0), (1, 0), (0, -1), (0, 1))
        return self.create_moves(board, output)

    def get_identificator(self) -> str:
        return self.color[0] + 'R'
