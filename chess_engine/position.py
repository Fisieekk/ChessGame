from pydantic import BaseModel


class Position(BaseModel):
    x: int
    y: int

    def in_board(self):
        return 0 <= self.x < 8 and 0 <= self.y < 8
