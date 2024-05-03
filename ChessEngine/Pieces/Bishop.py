from ChessEngine.Piece import Piece


class Bishop(Piece):
    def __init__(self, y: int, x: int, color: str):
        super().__init__(y, x, color)
        self.type = "Bishop"
        self.photo = "images/wB.png" if color == "white" else "images/bB.png"

    def can_move(self, map) -> tuple:
        return self.bishop_moves(map)

    def bishop_moves(self, map) -> tuple:
        output = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        return self.create_moves(map, output)

    def get_identificator(self) -> str:
        return self.color[0] + 'B'
