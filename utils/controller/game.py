import pygame
from chess_engine import *
from .game_config import GameConfig
from .game_controller import GameController


class Game:
    def __init__(self):
        self.config = GameConfig()
        self.map = Map(8, 8)
        self.controller = GameController(self.config, self.map)
        self.history = []
        self.captured_pieces = []
        self.moves = None
        self.attack_moves = None
        self.running = True
        self.selected_piece = None
        self.original_pos = None
        self.mouse_down = False
        self.config.LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.fps_counter = 0
        self.mate = False
        self.stalemate = False
        self.promoting_pieces = None
        self.config.load_images()

    # reinitialized board after clicking start
    def reinitialize(self) -> None:
        self.map = Map(8, 8)
        self.controller = GameController(self.config, self.map)
        self.history = []
        self.captured_pieces = []
        self.moves = None
        self.attack_moves = None
        self.running = True
        self.selected_piece = None
        self.original_pos = None
        self.mouse_down = False
        self.fps_counter = 0
        self.mate = False
        self.stalemate = False
        self.promoting_pieces = None

    def handle_promotion(self, x: int, y: int) -> None:
        for identifier, current_position in self.promoting_pieces:
            if current_position.collidepoint(x, y):
                self.map.change_piece(identifier)

    def select_piece(self, x: int, y: int) -> None:
        if (0 < x - self.config.X_OFFSET < self.config.BOARD_SIZE and
                0 < y - self.config.Y_OFFSET < self.config.BOARD_SIZE):
            row, col = (x - self.config.X_OFFSET) // self.config.SQUARE_SIZE, (
                    y - self.config.Y_OFFSET) // self.config.SQUARE_SIZE
            if self.map.board[col][row] and self.map.board[col][row].color == self.map.curr_player:
                self.selected_piece = self.map.board[col][row]
                self.original_pos = Position(x=row, y=col)
                self.mouse_down = True

    def update_possible_moves(self) -> None:
        if self.selected_piece:
            self.moves, self.attack_moves = self.selected_piece.can_move(self.map)
            if type(self.selected_piece) is King:
                self.moves, self.attack_moves = self.map.castle(self.moves, self.attack_moves, self.selected_piece)
            self.moves, self.attack_moves = self.map.preventer(self.moves, self.attack_moves, self.selected_piece)
        print('Moves: ', self.moves)
        print('Attack moves: ', self.attack_moves)

    def en_passant_verification(self, new_position: Position) -> bool:
        return (type(self.map.board[self.original_pos.y][self.original_pos.x]) is Pawn and new_position
                in self.attack_moves and type(self.map.board[self.original_pos.y][new_position.x]) is Pawn)

    def en_passant_move(self, new_position: Position) -> None:
        self.captured_pieces.append(self.map.board[self.original_pos.y][new_position.x].get_identificator())
        self.map.evaluate_captured_piece(self.map.board[self.original_pos.y][new_position.x])
        self.map.en_passant_move(self.original_pos, Position(x=new_position.x, y=new_position.y))

    def move(self, new_position: Position) -> None:
        if self.map.board[new_position.y][new_position.x]:
            self.captured_pieces.append(self.map.board[new_position.y][new_position.x].get_identificator())
            self.map.evaluate_captured_piece(self.map.board[new_position.y][new_position.x])

        self.map.move(self.original_pos, Position(x=new_position.x, y=new_position.y))

    def choose_type_of_move(self, x: int, y: int) -> None:
        if (0 < x - self.config.X_OFFSET < self.config.BOARD_SIZE and
                0 < y - self.config.Y_OFFSET < self.config.BOARD_SIZE):
            new_position = Position(x=((x - self.config.X_OFFSET) // self.config.SQUARE_SIZE),
                                    y=((y - self.config.Y_OFFSET) // self.config.SQUARE_SIZE))
            if new_position in self.moves or new_position in self.attack_moves:
                if self.original_pos.x != new_position.x or self.original_pos.y != new_position.y:
                    if self.en_passant_verification(new_position):
                        self.en_passant_move(new_position)
                    else:
                        self.move(new_position)
                    print('Captured value: ')
                    print('White: ', self.map.white_captured_value, ' Black: ',
                          self.map.black_captured_value)
                    move_id = self.selected_piece.get_identificator()[1] + self.config.LETTERS[new_position.x] + str(
                        8 - new_position.y)
                    self.map.history.append(move_id)
                    self.selected_piece.last_move = self.map.history[-1] if self.map.history else None
                    self.map.curr_player = 'white' if self.map.curr_player == 'black' else 'black'
                    self.map.check(self.map.curr_player)
                    self.mate = self.map.calculate_mate()
                    self.stalemate = self.map.calculate_stalemate()

        self.selected_piece = None
        self.moves, self.attack_moves = None, None
        self.mouse_down = False

    def reset_clicked(self, x, y) -> None:
        button_rect = pygame.Rect(self.config.START_BUTTON_X, self.config.START_BUTTON_Y, self.config.BUTTON_WIDTH,
                                  self.config.BUTTON_HEIGHT)
        if button_rect.collidepoint(x, y):
            self.reinitialize()


    def main(self) -> None:
        pygame.init()
        pygame.font.init()

        timer = pygame.time.Clock()
        pygame.display.set_caption('Chess App')

        while self.running:
            timer.tick(self.config.FPS)
            self.controller.update_screen()
            self.fps_counter += 1
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.reset_clicked(x, y)

                # if game not ended
                if not self.mate and not self.stalemate:
                    # and we don't have a promotion
                    if not self.map.promoting_piece:
                        # selecting a piece
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            self.select_piece(x, y)
                            self.update_possible_moves()

                        # if we have selected piece we can make a move
                        if event.type == pygame.MOUSEBUTTONUP and self.selected_piece:
                            x, y = pygame.mouse.get_pos()
                            self.choose_type_of_move(x, y)

            if self.mate:
                self.controller.draw_message('white' if self.map.curr_player == 'black' else 'black', None)

            elif self.stalemate:
                self.controller.draw_message(None, "Stalemate")

            if self.map.promoting_piece:
                self.promoting_pieces = self.controller.draw_promotion_options(self.map.promoting_piece.position)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.handle_promotion(x, y):
                        self.map.promoting_piece = None

                    # dragging piece
            if self.mouse_down and self.selected_piece:
                x, y = pygame.mouse.get_pos()
                self.controller.drag_piece(x, y, self.selected_piece)

            if self.mouse_down:
                self.controller.draw_possible_moves(self.moves, self.attack_moves)

            if self.map.check_white or self.map.check_black:
                self.controller.draw_checks()

            pygame.display.flip()

        pygame.quit()
