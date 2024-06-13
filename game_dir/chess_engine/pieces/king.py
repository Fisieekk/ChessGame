from chess_engine.piece import Piece
from .rook import Rook
from chess_engine.position import Position


class King(Piece):
    def __init__(self, y: int, x: int, color: str):
        super().__init__(y, x, color)
        self.type = "King"
        self.photo = "images/wK.png" if color == "white" else "images/bK.png"

    def can_move(self, map) -> tuple:
        """
        Method to get the possible moves of the piece.
        :param map: map of the game
        :return: tuple with the possible moves and the possible attacks
        """
        moves = []
        attack_moves = []
        castle_moves = self.castle(map)

        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                new_position = Position(x=self.position.x + j, y=self.position.y + i)
                if (i != 0 or j != 0) and new_position.in_board():
                    if map.board[new_position.y][new_position.x] is None:
                        moves.append(new_position)
                    else:
                        if (
                            map.board[new_position.y][new_position.x].color
                            != self.color
                        ):
                            attack_moves.append(new_position)

        moves += castle_moves
        return moves, attack_moves

    def can_castle(self, rook: Piece) -> bool:
        """
        Calculate if the king can castle with the rook.
        :param rook: rook to castle
        :return: True if the king can castle with the rook, False otherwise
        """
        return rook is not None and isinstance(rook, Rook) and not rook.has_moved

    def castle(self, map) -> list:
        """
        Get the possible castle moves.
        :param map: map of the game
        :return: possible castle moves
        """
        castle_moves = []
        left_rook = map.board[self.position.y][0]
        right_rook = map.board[self.position.y][7]
        if self.last_move is None:
            if self.can_castle(left_rook) and (
                map.board[self.position.y][1] is None
                and map.board[self.position.y][2] is None
                and map.board[self.position.y][3] is None
            ):
                castle_moves.append(Position(x=2, y=self.position.y))
            if self.can_castle(right_rook) and (
                map.board[self.position.y][5] is None
                and map.board[self.position.y][6] is None
            ):
                castle_moves.append(Position(x=6, y=self.position.y))

        return castle_moves

    def get_identificator(self) -> str:
        """
        Method to get the identificator of the piece.
        It creates a string with the first char of the color ("w" for "white" or "b" for "black") and the type of the piece.
        It is used to identify the photo of the piece.
        :return: identificator of the piece
        """
        return self.color[0] + "K"
