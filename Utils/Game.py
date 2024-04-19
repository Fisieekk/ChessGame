import pygame
import Utils.Map as mp
from Utils.Pieces.King import King


class Game:
    def __init__(self):
        self.BOARD_SIZE = 800
        self.ROW = 8
        self.COLUMN = 8
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 800
        self.X_OFFSET = 200
        self.Y_OFFSET = 0
        self.SQUARE_SIZE = 100
        self.IMAGES = {}
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.RED = (127, 0, 0, 128)
        self.DARK_RED = (255, 0, 0, 128)
        self.GREEN = (0, 128, 0, 128)
        self.BLACK = (0, 0, 0, 255)
        self.GREY = (200, 200, 200, 128)
        self.fps = 30
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.NOFRAME)
        self.gb = mp.Map(8, 8)
        self.history = []
        self.captured_pieces = []
        self.moves = None
        self.attack_moves = None
        self.mouse_down = False
        self.running = True
        self.selected_piece = None
        self.original_pos = None
        self.mouse_down = False
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.fps_counter = 0
        self.mate = False

    def load_images(self):
        pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(pygame.image.load('Utils/Images/' + piece + '.png'),
                                                        (self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_board(self):
        colors = [self.WHITE, self.GRAY]
        for r in range(self.ROW):
            for c in range(self.COLUMN):
                color = colors[((r + c) % 2)]
                pygame.draw.rect(self.screen, color,
                                 (self.X_OFFSET + c * self.SQUARE_SIZE, self.Y_OFFSET + r * self.SQUARE_SIZE,
                                  self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_pieces(self):
        for r in range(self.ROW):
            for c in range(self.COLUMN):
                piece = self.gb.board[r][c]
                if piece is not None:
                    self.screen.blit(self.IMAGES[piece.get_identificator()],
                                     pygame.Rect(self.X_OFFSET + c * self.SQUARE_SIZE,
                                                 self.Y_OFFSET + r * self.SQUARE_SIZE,
                                                 self.SQUARE_SIZE, self.SQUARE_SIZE))

    # we are never getting here
    def draw_possible_moves(self):
        for r, c in self.moves:
            move_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
            move_surface.fill(self.GREEN)
            self.screen.blit(move_surface, (self.X_OFFSET + c * self.SQUARE_SIZE, self.Y_OFFSET + r * self.SQUARE_SIZE))

        for r, c in self.attack_moves:
            attack_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
            attack_surface.fill(self.RED)
            self.screen.blit(attack_surface,
                             (self.X_OFFSET + c * self.SQUARE_SIZE, self.Y_OFFSET + r * self.SQUARE_SIZE))

    def show_checks(self):
        r, c = None, None
        if self.gb.check_white:
            r, c = self.gb.white_king_position
        elif self.gb.check_black:
            r, c = self.gb.black_king_position
        else:
            return
        move_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
        move_surface.fill(self.DARK_RED)
        self.screen.blit(move_surface, (self.X_OFFSET + c * self.SQUARE_SIZE, self.Y_OFFSET + r * self.SQUARE_SIZE))

    def show_message(self, color, message):
        message = color[0].upper() + color[1:] + ' won by checkmate'
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, self.BLACK)
        #text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        #self.screen.blit(text, text_rect)

    # gets screen and pawn to be promoted
    # returns new piece to be placed on board
    # TODO complete this function
    def handle_promotion(self, position):
        r, c = position
        color, positions = ('w', [7, 6, 5, 4]) if r == 7 else ('b', [0, 1, 2, 3])
        rectangles = [pygame.Rect(c * self.SQUARE_SIZE, r * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE) for r
                      in positions]
        identifiers = [color + x for x in ['Q', 'R', 'B', 'N']]
        for rectangle, identifier in zip(rectangles, identifiers):
            self.screen.blit(self.IMAGES[identifier], rectangle)
        return rectangles

    def select_piece(self, x, y):
        if 0 < x - self.X_OFFSET < self.BOARD_SIZE and 0 < y - self.Y_OFFSET < self.BOARD_SIZE:
            print(x, y)
            row, col = (x - self.X_OFFSET) // self.SQUARE_SIZE, (y - self.Y_OFFSET) // self.SQUARE_SIZE
            print(x,y)
            if self.gb.board[col][row] and self.gb.board[col][row].color == self.gb.curr_player:
                print(row, col)
                self.selected_piece = self.gb.board[col][row]
                self.original_pos = (col, row)
                print(self.selected_piece is not None)
                self.mouse_down = True

    def drag_piece(self, x, y):
        if 0 < x - self.X_OFFSET < self.BOARD_SIZE and 0 < y - self.Y_OFFSET < self.BOARD_SIZE:
            self.screen.blit(self.IMAGES[self.selected_piece.get_identificator()],
                             (x - self.SQUARE_SIZE // 2, y - self.SQUARE_SIZE // 2))

    def update_possible_moves(self):
        if self.selected_piece:
            moves, attack_moves = self.selected_piece.can_move(self.gb)
            self.moves, self.attack_moves = self.gb.preventer(moves, attack_moves, self.selected_piece)
            if type(self.selected_piece) == King:
                self.moves, self.attack_moves = self.gb.castle(self.moves, self.attack_moves, self.selected_piece)

    def make_move(self, x, y):
        if 0 < x - self.X_OFFSET < self.BOARD_SIZE and 0 < y - self.Y_OFFSET < self.BOARD_SIZE:
            new_row, new_col = (x - self.X_OFFSET) // self.SQUARE_SIZE, (
                    y - self.Y_OFFSET) // self.SQUARE_SIZE
            if [new_row, new_col] in self.moves or [new_row, new_col] in self.attack_moves:
                if self.original_pos[0] != new_row or self.original_pos[1] != new_col:
                    # only if new_pos contains other piece we are evaluating material, and adding to history
                    if self.gb.board[new_col][new_row]:
                        self.captured_pieces.append(self.gb.board[new_col][new_row].get_identificator())
                        self.gb.evaluate_captured_piece(self.gb.board[new_col][new_row])
                        print('Captured value: ')
                        print('White: ', self.gb.white_captured_value, ' Black: ',
                              self.gb.black_captured_value)
                        move_id = self.selected_piece.get_identificator()[1] + self.letters[new_row] + str(
                            8 - new_col)
                        self.gb.history.append(move_id)
                        self.selected_piece.last_move = self.gb.history[-1] if self.gb.history else None

                    self.gb.move(self.original_pos, (new_col, new_row))
                    self.gb.curr_player = 'white' if self.gb.curr_player == 'black' else 'black'
                    self.gb.check_white = self.gb.check_black = False

        self.selected_piece = None
        self.moves, self.attack_moves = None, None
        self.mouse_down = False

    def main(self):
        pygame.init()
        pygame.font.init()
        self.load_images()

        # pygame.display.set_caption("Chess")
        timer = pygame.time.Clock()

        while self.running:
            timer.tick(self.fps)
            self.draw_board()
            self.draw_pieces()
            self.fps_counter += 1
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    self.running = False

                # if game not ended
                elif not self.mate:
                    if not self.gb.promoting_piece:
                        # click on piece
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            self.select_piece(x, y)
                            # generate possible moves for selected piece depending on type
                            self.update_possible_moves()

                        # if we have selected piece we can make a move
                        if event.type == pygame.MOUSEBUTTONUP and self.selected_piece:
                            x, y = pygame.mouse.get_pos()
                            self.make_move(x, y)

                        # calculate mate TODO not working yet
                        self.mate = self.gb.calculate_mate(self.gb.curr_player)

                    # if promoting_piece is not none
                    else:
                        # show and handle promotion TODO not working yet
                        self.handle_promotion(self.gb.promoting_piece.position)


                else:
                    self.show_message('white' if self.gb.curr_player == 'black' else 'black', " ")

            # dragging piece
            if self.mouse_down and self.selected_piece:
                x, y = pygame.mouse.get_pos()
                self.drag_piece(x, y)

            if self.mouse_down:
                self.draw_possible_moves()
                # if self.gb.check_white or self.gb.check_black:
                #     self.show_checks()

            pygame.display.flip()

        pygame.quit()
