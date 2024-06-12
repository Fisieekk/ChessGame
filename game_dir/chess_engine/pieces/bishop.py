from game_dir.chess_engine.piece import Piece


class Bishop(Piece):
    def __init__(self, y: int, x: int, color: str):
        super().__init__(y, x, color)
        self.type = "Bishop"
        self.photo = "images/wB.png" if color == "white" else "images/bB.png"

    def can_move(self, map) -> tuple:
        """
        Method to get the possible moves of the piece.
        :param map: map of the game
        :return: tuple with the possible moves and the possible attacks
        """
        return self.bishop_moves(map)

    def bishop_moves(self, map) -> tuple:
        """
        Method to get the possible moves of the bishop.
        :param map: map of the game
        :return: tuple with the possible moves and the possible attacks
        """
        output = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        return self.create_moves(map, output)

    def get_identificator(self) -> str:
        """
        Method to get the identificator of the piece.
        It creates a string with the first char of the color ("w" for "white" or "b" for "black") and the type of the piece.
        It is used to identify the photo of the piece.
        :return: identificator of the piece
        """
        return self.color[0] + "B"
