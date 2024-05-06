import pygame
from chess_engine import *
from .GameConfig import GameConfig as gc
class Game:
    def __init__(self):
        self.IMAGES = {}
        self.map = Map(8, 8)
        self.history = []
        self.captured_pieces = []
        self.moves = None
        self.attack_moves = None
        self.running = True
        self.selected_piece = None
        self.original_pos = None
        self.mouse_down = False
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.fps_counter = 0
        self.mate = False
        self.stalemate = False
        self.promoting_pieces = None
        self.screen = pygame.display.set_mode((gc.WINDOW_WIDTH, gc.WINDOW_HEIGHT), )

    # reinitialized board after clicking start
    def reinitialize(self) -> None:
        self.map = Map(8, 8)
        self.history = []
        self.captured_pieces = []
        self.moves = None
        self.attack_moves = None
        self.running = True
        self.selected_piece = None
        self.original_pos = None
        self.mouse_down = False
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.fps_counter = 0
        self.mate = False
        self.stalemate = False
        self.promoting_pieces = None

    def load_images(self) -> None:
        pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(pygame.image.load('utils/images/' + piece + '.png'),
                                                        (gc.SQUARE_SIZE, gc.SQUARE_SIZE))

    def draw_board(self) -> None:
        colors = [gc.COLORS["WHITE"], gc.COLORS["GRAY"]]
        pygame.draw.rect(self.screen, gc.COLORS["BLACK"],
                         (gc.X_OFFSET - 1, gc.Y_OFFSET - 1, gc.BOARD_SIZE + 2, gc.BOARD_SIZE + 2), 2)
        for r in range(gc.ROW):
            for c in range(gc.COLUMN):
                color = colors[((r + c) % 2)]
                pygame.draw.rect(self.screen, color,
                                 (gc.X_OFFSET + c * gc.SQUARE_SIZE, gc.Y_OFFSET + r * gc.SQUARE_SIZE,
                                  gc.SQUARE_SIZE, gc.SQUARE_SIZE))

    def draw_pieces(self) -> None:
        for r in range(gc.ROW):
            for c in range(gc.COLUMN):
                piece = self.map.board[r][c]
                if piece is not None:
                    self.screen.blit(self.IMAGES[piece.get_identificator()],
                                     pygame.Rect(gc.X_OFFSET + c * gc.SQUARE_SIZE,
                                                 gc.Y_OFFSET + r * gc.SQUARE_SIZE,
                                                 gc.SQUARE_SIZE, gc.SQUARE_SIZE))

    # we are never getting here
    def draw_possible_moves(self) -> None:
        for move in self.moves:
            r,c=(move.y,move.x)
            move_surface = pygame.Surface((gc.SQUARE_SIZE, gc.SQUARE_SIZE), pygame.SRCALPHA)
            move_surface.fill(gc.COLORS["GREEN"])
            self.screen.blit(move_surface, (gc.X_OFFSET + c * gc.SQUARE_SIZE, gc.Y_OFFSET + r * gc.SQUARE_SIZE))

        for move in self.attack_moves:
            r, c = (move.y, move.x)
            attack_surface = pygame.Surface((gc.SQUARE_SIZE, gc.SQUARE_SIZE), pygame.SRCALPHA)
            attack_surface.fill(gc.COLORS["RED"])
            self.screen.blit(attack_surface,
                             (gc.X_OFFSET + c * gc.SQUARE_SIZE, gc.Y_OFFSET + r * gc.SQUARE_SIZE))

    def show_checks(self) -> None:
        r, c = None, None
        if self.map.check_white:
            r, c = self.map.white_king_position.y, self.map.white_king_position.x
        elif self.map.check_black:
            r, c = self.map.black_king_position.y, self.map.black_king_position.x
        else:
            return
        move_surface = pygame.Surface((gc.SQUARE_SIZE, gc.SQUARE_SIZE), pygame.SRCALPHA)
        move_surface.fill(gc.COLORS["DARK_RED"])
        self.screen.blit(move_surface, (gc.X_OFFSET + c * gc.SQUARE_SIZE, gc.Y_OFFSET + r * gc.SQUARE_SIZE))

    def show_message(self, color: str, message: str) -> None:
        if message is None:
            message = color[0].upper() + color[1:] + ' won by checkmate'
        font = pygame.font.Font(None, 72)
        text = font.render(message, True, gc.COLORS["GREEN"])
        text_rect = text.get_rect(center=(
            gc.X_OFFSET + gc.BOARD_SIZE // 2, gc.Y_OFFSET + gc.BOARD_SIZE // 2))
        self.screen.blit(text, text_rect)

    def show_promotion_options(self, position: Position) -> None:
        c,r = position.x, position.y
        color, positions = ('b', [2, 3, 4, 5]) if r == 7 else ('w', [5, 4, 3, 2])
        r = -1.1 if r == 0 else 8.1
        rectangles = [
            pygame.Rect(gc.X_OFFSET + c * gc.SQUARE_SIZE, gc.Y_OFFSET + r * gc.SQUARE_SIZE, gc.SQUARE_SIZE,
                        gc.SQUARE_SIZE) for c in positions]
        identifiers = [color + x for x in ['Q', 'R', 'B', 'N']]
        self.promoting_pieces = []
        for rectangle, identifier in zip(rectangles, identifiers):
            self.screen.blit(self.IMAGES[identifier], rectangle)
            self.promoting_pieces.append((identifier, rectangle))

    def handle_promotion(self, x: int, y: int) -> None:
        for identifier, position in self.promoting_pieces:
            if position.collidepoint(x, y):
                self.map.change_piece(identifier)

    def select_piece(self, x: int, y: int) -> None:
        if 0 < x - gc.X_OFFSET < gc.BOARD_SIZE and 0 < y - gc.Y_OFFSET < gc.BOARD_SIZE:
            row, col = (x - gc.X_OFFSET) // gc.SQUARE_SIZE, (y - gc.Y_OFFSET) // gc.SQUARE_SIZE
            if self.map.board[col][row] and self.map.board[col][row].color == self.map.curr_player:
                self.selected_piece = self.map.board[col][row]
                self.original_pos = Position(x=row, y=col)
                self.mouse_down = True

    def drag_piece(self, x: int, y: int) -> None:
        if 0 < x - gc.X_OFFSET < gc.BOARD_SIZE and 0 < y - gc.Y_OFFSET < gc.BOARD_SIZE:
            self.screen.blit(self.IMAGES[self.selected_piece.get_identificator()],
                             (x - gc.SQUARE_SIZE // 2, y - gc.SQUARE_SIZE // 2))

    def update_possible_moves(self) -> None:
        if self.selected_piece:
            self.moves, self.attack_moves = self.selected_piece.can_move(self.map)
            if type(self.selected_piece) == King:
                self.moves, self.attack_moves = self.map.castle(self.moves, self.attack_moves, self.selected_piece)
            self.moves, self.attack_moves = self.map.preventer(self.moves, self.attack_moves, self.selected_piece)
        print('Moves: ', self.moves)
        print('Attack moves: ', self.attack_moves)

    def en_passant_verification(self, new_position: Position) -> bool:
        return (type(self.map.board[self.original_pos.y][self.original_pos.x]) == Pawn and new_position
                in self.attack_moves and type(self.map.board[self.original_pos.y][new_position.x]) == Pawn)

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
        if 0 < x - gc.X_OFFSET < gc.BOARD_SIZE and 0 < y - gc.Y_OFFSET < gc.BOARD_SIZE:
            new_position = Position(x=((x - gc.X_OFFSET) // gc.SQUARE_SIZE), y=((y - gc.Y_OFFSET) // gc.SQUARE_SIZE))
            if new_position in self.moves or new_position in self.attack_moves:
                if self.original_pos.x != new_position.x or self.original_pos.y != new_position.y:
                    if self.en_passant_verification(new_position):
                        self.en_passant_move(new_position)
                    else:
                        self.move(new_position)
                    print('Captured value: ')
                    print('White: ', self.map.white_captured_value, ' Black: ',
                          self.map.black_captured_value)
                    move_id = self.selected_piece.get_identificator()[1] + self.letters[new_position.x] + str(
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

    def draw_reset_button(self) -> None:
        font = pygame.font.SysFont(None, 64)
        text = font.render('RESET', True, gc.COLORS["BLACK"])
        text_rect = text.get_rect(
            center=(gc.START_BUTTON_X + gc.BUTTON_WIDTH // 2, gc.START_BUTTON_Y + gc.BUTTON_HEIGHT // 2))

        mouse_pos = pygame.mouse.get_pos()
        is_mouse_over = pygame.Rect(gc.START_BUTTON_X, gc.START_BUTTON_Y, gc.BUTTON_WIDTH,
                                    gc.BUTTON_HEIGHT).collidepoint(mouse_pos)

        if is_mouse_over and pygame.mouse.get_pressed()[0]:
            button_color = gc.COLORS["GRAY"]
        else:
            button_color = gc.COLORS["LIGHT_GRAY"]

        pygame.draw.rect(self.screen, button_color,
                         (gc.START_BUTTON_X, gc.START_BUTTON_Y, gc.BUTTON_WIDTH, gc.BUTTON_HEIGHT))
        pygame.draw.rect(self.screen, gc.COLORS["BLACK"],
                         (gc.START_BUTTON_X, gc.START_BUTTON_Y, gc.BUTTON_WIDTH, gc.BUTTON_HEIGHT), 2)
        self.screen.blit(text, text_rect)

    def draw_undo_button(self) -> None:
        font = pygame.font.SysFont(None, 64)
        text = font.render('UNDO', True, gc.COLORS["BLACK"])
        text_rect = text.get_rect(
            center=(gc.UNDO_BUTTON_X + gc.BUTTON_WIDTH // 2, gc.UNDO_BUTTON_Y + gc.BUTTON_HEIGHT // 2))

        mouse_pos = pygame.mouse.get_pos()
        is_mouse_over = pygame.Rect(gc.UNDO_BUTTON_X, gc.UNDO_BUTTON_Y, gc.BUTTON_WIDTH,
                                    gc.BUTTON_HEIGHT).collidepoint(mouse_pos)

        if is_mouse_over and pygame.mouse.get_pressed()[0]:
            button_color = gc.COLORS["GRAY"]
        else:
            button_color = gc.COLORS["LIGHT_GRAY"]

        pygame.draw.rect(self.screen, button_color,
                         (gc.UNDO_BUTTON_X, gc.UNDO_BUTTON_Y, gc.BUTTON_WIDTH, gc.BUTTON_HEIGHT))
        pygame.draw.rect(self.screen, gc.COLORS["BLACK"],
                         (gc.UNDO_BUTTON_X, gc.UNDO_BUTTON_Y, gc.BUTTON_WIDTH, gc.BUTTON_HEIGHT), 2)
        self.screen.blit(text, text_rect)

    def draw_material_diff(self) -> None:
        ratio = (self.map.black_captured_value + 10) / (
                self.map.black_captured_value + 20 + self.map.white_captured_value)
        b_x, b_y = gc.X_OFFSET - 2 * gc.MATERIAL_CHART_WIDTH, gc.Y_OFFSET
        w_x, w_y = b_x, b_y + int(ratio * gc.BOARD_SIZE)
        b_x_diff, b_y_diff = gc.MATERIAL_CHART_WIDTH, w_y
        w_x_diff, w_y_diff = gc.MATERIAL_CHART_WIDTH, gc.Y_OFFSET + gc.BOARD_SIZE - w_y
        pygame.draw.rect(self.screen, (0, 0, 0), (b_x, b_y, b_x_diff, b_y_diff))

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (b_x, w_y, w_x_diff, w_y_diff))

    def draw_utils(self) -> None:
        self.draw_reset_button()
        self.draw_undo_button()
        self.draw_material_diff()

    def reset_clicked(self, x, y) -> None:
        button_rect = pygame.Rect(gc.START_BUTTON_X, gc.START_BUTTON_Y, gc.BUTTON_WIDTH,
                                  gc.BUTTON_HEIGHT)
        if button_rect.collidepoint(x, y):
            self.reinitialize()

    # # TODO Implement undo_clicked
    # def undo_clicked(self) :
    #     pass

    def main(self) -> None:
        pygame.init()
        pygame.font.init()
        self.load_images()
        timer = pygame.time.Clock()
        pygame.display.set_caption('Chess App')

        while self.running:
            timer.tick(gc.fps)
            self.screen.fill(gc.COLORS["BEIGE"])
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
                self.show_message('white' if self.map.curr_player == 'black' else 'black', None)

            elif self.stalemate:
                self.show_message(None, "Stalemate")

            if self.map.promoting_piece:
                self.show_promotion_options(self.map.promoting_piece.position)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.handle_promotion(x, y):
                        self.map.promoting_piece = None

                    # dragging piece
            if self.mouse_down and self.selected_piece:
                x, y = pygame.mouse.get_pos()
                self.drag_piece(x, y)

            if self.mouse_down:
                self.draw_possible_moves()
            if self.map.check_white or self.map.check_black:
                self.show_checks()

            pygame.display.flip()

        pygame.quit()
