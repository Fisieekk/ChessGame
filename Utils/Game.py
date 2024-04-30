import pygame
import Utils.Map as mp
from Utils.Pieces.King import King
from Utils.Pieces.Pawn import Pawn

class Game:
    def __init__(self):
        self.ROW = 8
        self.COLUMN = 8
        self.WINDOW_WIDTH = 1100
        self.WINDOW_HEIGHT = 800
        self.X_OFFSET = 100
        self.Y_OFFSET = 100
        self.SQUARE_SIZE = 75
        self.BOARD_SIZE = 8 * self.SQUARE_SIZE
        self.START_BUTTON_X = self.X_OFFSET + self.BOARD_SIZE + 100
        self.START_BUTTON_Y = self.Y_OFFSET + 120
        self.UNDO_BUTTON_X = self.X_OFFSET + self.BOARD_SIZE + 100
        self.UNDO_BUTTON_Y = self.Y_OFFSET + 3 * self.SQUARE_SIZE + 150
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 100
        self.MATERIAL_CHART_WIDTH = 20
        self.IMAGES = {}
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.RED = (127, 0, 0, 128)
        self.DARK_RED = (255, 0, 0, 128)
        self.GREEN = (0, 128, 0, 128)
        self.BLACK = (0, 0, 0, 255)
        self.LIGHT_GRAY = (169, 169, 169)
        self.BEIGE = (255, 246, 231)
        self.fps = 30
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), )
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
        self.stalemate=False
        self.promoting_pieces = None

    # reinitializes board after clicking start
    def reinitialize(self):
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
        self.stalemate=False
        self.promoting_pieces = None

    def load_images(self):
        pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(pygame.image.load('Utils/Images/' + piece + '.png'),
                                                        (self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_board(self):
        colors = [self.WHITE, self.GRAY]
        pygame.draw.rect(self.screen, self.BLACK,
                         (self.X_OFFSET - 1, self.Y_OFFSET - 1, self.BOARD_SIZE + 2, self.BOARD_SIZE + 2), 2)
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
        if message is None:
            message = color[0].upper() + color[1:] + ' won by checkmate'
        font = pygame.font.Font(None, 72)
        text = font.render(message, True, self.GREEN)
        text_rect = text.get_rect(center=(
            self.X_OFFSET + self.BOARD_SIZE // 2, self.Y_OFFSET + self.BOARD_SIZE // 2))
        self.screen.blit(text, text_rect)

    def show_promotion(self, position):
        r, c = position
        color, positions = ('b', [2, 3, 4, 5]) if r == 7 else ('w', [5, 4, 3, 2])
        r = -1.1 if r == 0 else 8.1
        rectangles = [
            pygame.Rect(self.X_OFFSET + c * self.SQUARE_SIZE, self.Y_OFFSET + r * self.SQUARE_SIZE, self.SQUARE_SIZE,
                        self.SQUARE_SIZE) for c in positions]
        identifiers = [color + x for x in ['Q', 'R', 'B', 'N']]
        self.promoting_pieces = []
        for rectangle, identifier in zip(rectangles, identifiers):
            self.screen.blit(self.IMAGES[identifier], rectangle)
            self.promoting_pieces.append((identifier, rectangle))

    def handle_promotion(self, x, y):
        for identifier, position in self.promoting_pieces:
            if position.collidepoint(x, y):
                self.gb.change_piece(identifier)
                return

    def select_piece(self, x, y):
        if 0 < x - self.X_OFFSET < self.BOARD_SIZE and 0 < y - self.Y_OFFSET < self.BOARD_SIZE:
            row, col = (x - self.X_OFFSET) // self.SQUARE_SIZE, (y - self.Y_OFFSET) // self.SQUARE_SIZE
            if self.gb.board[col][row] and self.gb.board[col][row].color == self.gb.curr_player:
                self.selected_piece = self.gb.board[col][row]
                self.original_pos = (col, row)
                self.mouse_down = True

    def drag_piece(self, x, y):
        if 0 < x - self.X_OFFSET < self.BOARD_SIZE and 0 < y - self.Y_OFFSET < self.BOARD_SIZE:
            self.screen.blit(self.IMAGES[self.selected_piece.get_identificator()],
                             (x - self.SQUARE_SIZE // 2, y - self.SQUARE_SIZE // 2))

    def update_possible_moves(self):
        if self.selected_piece:
            self.moves, self.attack_moves = self.selected_piece.can_move(self.gb)
            if type(self.selected_piece) == King:
                self.moves, self.attack_moves = self.gb.castle(self.moves, self.attack_moves, self.selected_piece)
            self.moves, self.attack_moves = self.gb.preventer(self.moves, self.attack_moves, self.selected_piece)

    def make_move(self, x, y):
        if 0 < x - self.X_OFFSET < self.BOARD_SIZE and 0 < y - self.Y_OFFSET < self.BOARD_SIZE:
            new_col, new_row = (x - self.X_OFFSET) // self.SQUARE_SIZE, (y - self.Y_OFFSET) // self.SQUARE_SIZE
            if [new_row, new_col] in self.moves or [new_row, new_col] in self.attack_moves:
                if self.original_pos[1] != new_col or self.original_pos[0] != new_row:
                    if type(self.gb.board[self.original_pos[0]][self.original_pos[1]])==Pawn and [new_row,new_col] in self.attack_moves and type(self.gb.board[self.original_pos[0]][new_col])==Pawn:
                        self.captured_pieces.append(self.gb.board[self.original_pos[0]][new_col].get_identificator())
                        self.gb.evaluate_captured_piece(self.gb.board[self.original_pos[0]][new_col])
                        print('Captured value: ')
                        print('White: ', self.gb.white_captured_value, ' Black: ',
                            self.gb.black_captured_value)
                        move_id = self.selected_piece.get_identificator()[1] + self.letters[new_col] + str(
                            8 - new_row)
                        self.gb.history.append(move_id)
                        self.selected_piece.last_move = self.gb.history[-1] if self.gb.history else None 
                        self.gb.en_passant_move(self.original_pos, (new_row, new_col))
                    else:
                        if self.gb.board[new_row][new_col]:
                            self.captured_pieces.append(self.gb.board[new_row][new_col].get_identificator())
                            self.gb.evaluate_captured_piece(self.gb.board[new_row][new_col])
                            print('Captured value: ')
                            print('White: ', self.gb.white_captured_value, ' Black: ',
                                self.gb.black_captured_value)
                            move_id = self.selected_piece.get_identificator()[1] + self.letters[new_col] + str(
                                8 - new_row)
                            self.gb.history.append(move_id)
                            self.selected_piece.last_move = self.gb.history[-1] if self.gb.history else None

                        self.gb.move(self.original_pos, (new_row, new_col))
                    self.gb.curr_player = 'white' if self.gb.curr_player == 'black' else 'black'
                    self.gb.check(self.gb.curr_player)
                    self.mate = self.gb.calculate_mate()
                    self.stalemate= self.gb.calculate_stalemate()

        self.selected_piece = None
        self.moves, self.attack_moves = None, None
        self.mouse_down = False

    def draw_reset_button(self):
        font = pygame.font.SysFont(None, 64)
        text = font.render('RESET', True, self.BLACK)
        text_rect = text.get_rect(
            center=(self.START_BUTTON_X + self.BUTTON_WIDTH // 2, self.START_BUTTON_Y + self.BUTTON_HEIGHT // 2))

        mouse_pos = pygame.mouse.get_pos()
        is_mouse_over = pygame.Rect(self.START_BUTTON_X, self.START_BUTTON_Y, self.BUTTON_WIDTH,
                                    self.BUTTON_HEIGHT).collidepoint(mouse_pos)

        if is_mouse_over and pygame.mouse.get_pressed()[0]:
            button_color = self.GRAY
        else:
            button_color = self.LIGHT_GRAY

        pygame.draw.rect(self.screen, button_color,
                         (self.START_BUTTON_X, self.START_BUTTON_Y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT))
        pygame.draw.rect(self.screen, self.BLACK,
                         (self.START_BUTTON_X, self.START_BUTTON_Y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT), 2)
        self.screen.blit(text, text_rect)

    def draw_undo_button(self):
        font = pygame.font.SysFont(None, 64)
        text = font.render('UNDO', True, self.BLACK)
        text_rect = text.get_rect(
            center=(self.UNDO_BUTTON_X + self.BUTTON_WIDTH // 2, self.UNDO_BUTTON_Y + self.BUTTON_HEIGHT // 2))

        mouse_pos = pygame.mouse.get_pos()
        is_mouse_over = pygame.Rect(self.UNDO_BUTTON_X, self.UNDO_BUTTON_Y, self.BUTTON_WIDTH,
                                    self.BUTTON_HEIGHT).collidepoint(mouse_pos)

        if is_mouse_over and pygame.mouse.get_pressed()[0]:
            button_color = self.GRAY
        else:
            button_color = self.LIGHT_GRAY

        pygame.draw.rect(self.screen, button_color,
                         (self.UNDO_BUTTON_X, self.UNDO_BUTTON_Y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT))
        pygame.draw.rect(self.screen, self.BLACK,
                         (self.UNDO_BUTTON_X, self.UNDO_BUTTON_Y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT), 2)
        self.screen.blit(text, text_rect)

    def draw_material_diff(self):
        ratio = (self.gb.black_captured_value + 10) / (self.gb.black_captured_value + 20 + self.gb.white_captured_value)
        b_x, b_y = self.X_OFFSET - 2 * self.MATERIAL_CHART_WIDTH, self.Y_OFFSET
        w_x, w_y = b_x, b_y + int(ratio * self.BOARD_SIZE)
        b_x_diff, b_y_diff=self.MATERIAL_CHART_WIDTH, w_y
        w_x_diff, w_y_diff = self.MATERIAL_CHART_WIDTH, self.Y_OFFSET + self.BOARD_SIZE-w_y
        pygame.draw.rect(self.screen, (0, 0, 0), (b_x, b_y,b_x_diff, b_y_diff ))

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (b_x, w_y,w_x_diff, w_y_diff))

    def draw_utils(self):
        self.draw_reset_button()
        self.draw_undo_button()
        self.draw_material_diff()

    def reset_clicked(self, x, y):
        button_rect = pygame.Rect(self.START_BUTTON_X, self.START_BUTTON_Y, self.BUTTON_WIDTH,
                                  self.BUTTON_HEIGHT)
        if button_rect.collidepoint(x, y):
            self.reinitialize()

    # TODO Implement undo_clicked
    def undo_clicked(self):
        pass

    def main(self):
        pygame.init()
        pygame.font.init()
        self.load_images()
        timer = pygame.time.Clock()
        pygame.display.set_caption('Chess App')

        while self.running:
            timer.tick(self.fps)
            self.screen.fill(self.BEIGE)
            self.draw_board()
            self.draw_pieces()
            self.draw_utils()
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
                    if not self.gb.promoting_piece:
                        # selecting a piece
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            self.select_piece(x, y)
                            self.update_possible_moves()

                        # if we have selected piece we can make a move
                        if event.type == pygame.MOUSEBUTTONUP and self.selected_piece:
                            x, y = pygame.mouse.get_pos()
                            self.make_move(x, y)

            if self.mate:
                self.show_message('white' if self.gb.curr_player == 'black' else 'black', None)

            elif self.stalemate:
                self.show_message(None, "Stalemate")

            if self.gb.promoting_piece:
                self.show_promotion(self.gb.promoting_piece.position)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.handle_promotion(x, y):
                        self.gb.promoting_piece = None

                    # dragging piece
            if self.mouse_down and self.selected_piece:
                x, y = pygame.mouse.get_pos()
                self.drag_piece(x, y)

            if self.mouse_down:
                self.draw_possible_moves()
            if self.gb.check_white or self.gb.check_black:
                self.show_checks()

            pygame.display.flip()

        pygame.quit()
