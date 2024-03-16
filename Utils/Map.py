from .Pieces.Bishop import Bishop
from .Pieces.King import King
from .Pieces.Knight import Knight
from .Pieces.Pawn import Pawn
from .Pieces.Queen import Queen
from .Pieces.Rook import Rook


class Map:
    def __init__(self, width, height):
        self.curr_player = 'white'
        self.moves=[]
        self.turn=1
        self.promotion=None
        self.check_white=False
        self.check_black=False
        self.winner=None
        self.width = width
        self.height = height
        self.board = [
            [Rook((0,0),'black'), Knight((0,1),'black'), Bishop((0,2),'black'), Queen((0,3),'black'), King((0,4),'black'), Bishop((0,5),'black'), Knight((0,6),'black'), Rook((0,7),'black')],
            [Pawn((1,0),'black'), Pawn((1,1),'black'), Pawn((1,2),'black'), Pawn((1,3),'black'), Pawn((1,4),'black'), Pawn((1,5),'black'), Pawn((1,6),'black'), Pawn((1,7),'black')],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn((6,0),'white'), Pawn((6,1),'white'), Pawn((6,2),'white'), Pawn((6,3),'white'), Pawn((6,4),'white'), Pawn((6,5),'white'), Pawn((6,6),'white'), Pawn((6,7),'white')],
            [Rook((7,0),'white'), Knight((7,1),'white'), Bishop((7,2),'white'), Queen((7,3),'white'), King((7,4),'white'), Bishop((7,5),'white'), Knight((7,6),'white'), Rook((7,7),'white')]
        ]
