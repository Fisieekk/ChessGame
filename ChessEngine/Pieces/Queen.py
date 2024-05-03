from ChessEngine.Piece import Piece
from .Bishop import Bishop
from .Rook import Rook


class Queen(Piece):
    def __init__(self, y: int, x: int, color: str):
        super().__init__(y, x, color)
        self.type = "Queen"
        self.photo = "Images/wQ.png" if color == "white" else "Images/bQ.png"

    def can_move(self, map) -> tuple:
        bishop = Bishop(self.position.y, self.position.x, self.color)
        rook = Rook(self.position.y, self.position.x, self.color)
        moves, attack_moves = rook.can_move(map)
        moves += bishop.can_move(map)[0]
        attack_moves += bishop.can_move(map)[1]
        return moves, attack_moves

    def get_identificator(self) -> str:
        return self.color[0] + 'Q'
