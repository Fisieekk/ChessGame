from Map import Map
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Map(screen)
        self.selected_piece = None
        self.selected_piece_moves = []
        self.selected_piece_attack_moves = []
        self.selected_original_position = None
        self.dragged_piece = None
        self.mouse_x = 0
        self.mouse_y = 0
        