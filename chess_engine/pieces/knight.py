from chess_engine.piece import Piece, Position


class Knight(Piece):
    def __init__(self, y: int, x: int, color: str):
        super().__init__(y, x, color)
        self.type = "Knight"
        self.photo = "images/wN.png" if color == "white" else "images/bN.png"

    def can_move(self, map) -> tuple:
        """
        Method to get the possible moves of the piece.
        :param map: map of the game
        :return: tuple with the possible moves and the possible attacks
        """
        moves = []
        attack_moves = []
        moves_comb = [-2, -1, 1, 2]
        for i in moves_comb:
            for j in moves_comb:
                new_position = Position(x=self.position.x + i, y=self.position.y + j)
                if abs(i) != abs(j) and new_position.in_board():
                    if map.board[new_position.y][new_position.x] is None:
                        moves.append(new_position)
                    else:
                        if (
                            map.board[new_position.y][new_position.x].color
                            != self.color
                        ):
                            attack_moves.append(new_position)
        return moves, attack_moves

    def get_identificator(self) -> str:
        """
        Method to get the identificator of the piece.
        It creates a string with the first char of the color ("w" for "white" or "b" for "black") and the type of the piece.
        It is used to identify the photo of the piece.
        :return: identificator of the piece
        """
        return self.color[0] + "N"
