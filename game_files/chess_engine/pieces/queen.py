from game_files.chess_engine.piece import Piece
from game_files.chess_engine.pieces.bishop import Bishop
from game_files.chess_engine.pieces.rook import Rook


class Queen(Piece):
    def __init__(self, y: int, x: int, color: str):
        super().__init__(y, x, color)
        self.type = "Queen"
        self.photo = "images/wQ.png" if color == "white" else "images/bQ.png"

    def can_move(self, map) -> tuple:
        """
        Method to get the possible moves of the piece.
        :param map: map of the game
        :return: tuple with the possible moves and the possible attacks
        """
        bishop = Bishop(self.position.y, self.position.x, self.color)
        rook = Rook(self.position.y, self.position.x, self.color)
        moves, attack_moves = rook.can_move(map)
        moves += bishop.can_move(map)[0]
        attack_moves += bishop.can_move(map)[1]
        return moves, attack_moves

    def get_identificator(self) -> str:
        """
        Method to get the identificator of the piece.
        It creates a string with the first char of the color ("w" for "white" or "b" for "black") and the type of the piece.
        It is used to identify the photo of the piece.
        :return: identificator of the piece
        """
        return self.color[0] + "Q"
