from pydantic import BaseModel


class Position(BaseModel):
    x: int
    y: int

    def in_board(self) -> bool:
        """
        Check if the position is in the board
        :return: True if the position is in the board, False otherwise
        """
        return 0 <= self.x < 8 and 0 <= self.y < 8

    def from_string_to_map(self, position: str):
        """
        Set the position from a string
        :param position: The string position
        """
        self.x = ord(position[0]) - ord('a')
        self.y = 8-int(position[1])
