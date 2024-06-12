from game_files.chess_engine.piece import Piece
from game_files.chess_engine.position import Position


class Pawn(Piece):
    def __init__(self, y: int, x: int, color: str):
        super().__init__(y, x, color)
        self.type = "Pawn"
        self.photo = "images/wp.png" if color == "white" else "images/bp.png"

    def can_move(self, map) -> tuple:
        """
        Method to get the possible moves of the piece.
        :param map: map of the game
        :return: tuple with the possible moves and the possible attacks
        """
        if self.color == "white":
            position_change = -1
        else:
            position_change = 1
        moves = []
        attack_moves = []
        new_position = Position(x=self.position.x, y=self.position.y + position_change)
        if (
            new_position.in_board()
            and map.board[new_position.y][new_position.x] is None
        ):
            moves.append(new_position)
            if self.last_move is None:
                new_position = Position(
                    x=new_position.x, y=new_position.y + position_change
                )
                if map.board[new_position.y][new_position.x] is None:
                    moves.append(new_position)
        for i in (-1, 1):
            new_position = Position(
                x=self.position.x + i, y=self.position.y + position_change
            )
            if (
                new_position.in_board()
                and map.board[new_position.y][new_position.x]
                and map.board[new_position.y][new_position.x].color != self.color
            ):
                attack_moves.append(new_position)
            if map.last_move:
                if new_position.in_board() and self.en_passant_verification(
                    map, new_position, position_change
                ):
                    attack_moves.append(new_position)
        return moves, attack_moves

    def en_passant_verification(
        self, map, new_position: Position, position_change: int
    ) -> bool:
        """
        Method to verify if the en passant move is possible.
        :param map: map of the game
        :param new_position: new position of the piece
        :param position_change: change of the position of the piece when en passant move is possible
        :return: True if the en passant move is possible, False otherwise
        """
        return (
            self.position.y == map.last_move[1].y
            and new_position.y == map.last_move[1].y + position_change
            and new_position.x == map.last_move[1].x
            and type(map.last_move[2]) == Pawn
            and map.last_move[2].color != self.color
            and abs(map.last_move[1].y - map.last_move[0].y) == 2
        )

    def get_identificator(self) -> str:
        """
        Method to get the identificator of the piece.
        It creates a string with the first char of the color ("w" for "white" or "b" for "black") and the type of the piece.
        It is used to identify the photo of the piece.
        :return: identificator of the piece
        """
        return self.color[0] + "P"
