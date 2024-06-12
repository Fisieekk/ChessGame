from game_dir.chess_engine.piece import Piece


class Rook(Piece):
    def __init__(self, y: int, x: int, color: str):
        super().__init__(y, x, color)
        self.type = "Rook"
        self.photo = "images/wR.png" if color == "white" else "images/bR.png"

    def can_move(self, map) -> tuple:
        """
        Method to get the possible moves of the piece.
        :param map: map of the game
        :return: tuple with the possible moves and the possible attacks
        """
        return self.rook_moves(map)

    def rook_moves(self, board) -> tuple:
        """
        Method to get the possible moves of the rook
        :param board: board of the game
        :return: tuple with the possible moves and the possible attacks
        """
        output = ((-1, 0), (1, 0), (0, -1), (0, 1))
        return self.create_moves(board, output)

    def get_identificator(self) -> str:
        """
        Method to get the identificator of the piece.
        It creates a string with the first char of the color ("w" for "white" or "b" for "black") and the type of the piece.
        It is used to identify the photo of the piece.
        :return: identificator of the piece
        """
        return self.color[0] + "R"
