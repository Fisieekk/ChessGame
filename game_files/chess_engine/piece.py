import pygame
from game_files.chess_engine.position import Position


class Piece:
    def __init__(self, y: int, x: int, color: str):
        self.position = Position(x=x, y=y)
        self.color = color
        self.has_moved = False
        self.picture = None
        self.last_move = None

    def get_picture(self) -> pygame.image:
        """
        Get the picture of the piece
        :return: pygame.image representing the piece
        """
        return self.picture

    def get_last_move(self) -> Position:
        """
        Get the last move of the piece
        :return: position of the last move
        """
        return self.last_move

    def move(self, position: Position) -> None:
        """
        Move the piece to the given position
        :param position: Position to move the piece to
        :return: None
        """
        self.position = position
        self.has_moved = True

    def create_moves(self, map, output: list) -> tuple:
        """
        Create the moves of the piece
        :param map: map of the game
        :param output: list of moves
        :return: tuple of moves and attack moves
        """
        moves = []
        attack_moves = []
        for move in output:
            new_position = Position(
                x=self.position.x + move[1], y=self.position.y + move[0]
            )
            while (
                new_position.in_board()
                and map.board[new_position.y][new_position.x] is None
            ):
                moves.append(new_position)
                new_position = Position(
                    x=new_position.x + move[1], y=new_position.y + move[0]
                )

            if (
                8 > new_position.x >= 0
                and 8 > new_position.y >= 0
                and map.board[new_position.y][new_position.x] is not None
                and map.board[new_position.y][new_position.x].color != self.color
            ):
                attack_moves.append(new_position)

        return moves, attack_moves

    def get_identificator(self) -> str:
        """
        Method to get the identificator of the piece. We are overriding this method in the subclasses.
        It creates a string with the first char of the color ("w" for "white" or "b" for "black") and the type of the piece.
        It is used to identify the photo of the piece.
        :return: identificator of the piece
        """
        pass
