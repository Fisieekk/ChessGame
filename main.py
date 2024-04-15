import pygame
import Utils.Map as mp
from Utils.Pieces.King import King

# Added some features:
#  not validated piece moving showing possible moves (TODO implement method to return possible moves, for now there are some random positions selected)
#  move history
#  I need to refactor main function because now it's not intuitive and messy, especially main loop
#  TODO be careful about order (board[col][row])!

# TODO maybe move to Map?
WIDTH, HEIGHT = 800, 800
ROW, COLUMN = 8, 8
SIZE = WIDTH // ROW
IMAGES = {}
# Define colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (127, 0, 0, 128)
DARK_RED = (255, 0, 0, 128)
GREEN = (0, 128, 0, 128)
fps = 30


def load_images():
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('Utils/Images/' + piece + '.png'), (SIZE, SIZE))


def draw_board(screen):
    colors = [WHITE, GRAY]
    for r in range(ROW):
        for c in range(COLUMN):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, (c * SIZE, r * SIZE, SIZE, SIZE))


def draw_pieces(screen, board):
    for r in range(ROW):
        for c in range(COLUMN):
            piece = board[r][c]
            if piece is not None:
                screen.blit(IMAGES[piece.get_identificator()], pygame.Rect(c * SIZE, r * SIZE, SIZE, SIZE))


# draws all the possible moves and attack moves
def draw_possible_moves(screen, moves, attack_moves):
    for r, c in moves:
        move_surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
        move_surface.fill(GREEN)
        screen.blit(move_surface, (c * SIZE, r * SIZE))

    for r, c in attack_moves:
        attack_surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
        attack_surface.fill(RED)
        screen.blit(attack_surface, (c * SIZE, r * SIZE))


def show_checks(screen, gb):
    r, c = None, None
    if gb.check_white:
        r, c = gb.white_king_position
    elif gb.check_black:
        r, c = gb.black_king_position
    else:
        return
    move_surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    move_surface.fill(DARK_RED)
    screen.blit(move_surface, (c * SIZE, r * SIZE))


# TODO refactor main function
def main():
    pygame.init()
    pygame.font.init()
    load_images()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    gb = mp.Map(8, 8)
    board = gb.board
    history = []
    captured_pieces = []

    pygame.display.set_caption("Chess")
    timer = pygame.time.Clock()
    running = True
    selected_piece = None
    original_pos = None
    mouse_down = False
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    fps_counter = 0

    while running:
        timer.tick(fps)
        draw_board(screen)
        draw_pieces(screen, board)
        fps_counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = x // SIZE, y // SIZE
                if board[col][row] and board[col][row].color == gb.curr_player:
                    selected_piece = board[col][row]
                    original_pos = (col, row)
                    mouse_down = True

            # here is a place for move validation
            if event.type == pygame.MOUSEBUTTONUP and selected_piece:
                x, y = pygame.mouse.get_pos()
                new_col, new_row = y // SIZE, x // SIZE
                # board[original_pos[0]][original_pos[1]] = None

                if board[new_col][new_row]:
                    captured_pieces.append(board[new_col][new_row].get_identificator())
                # board[new_col][new_row] = selected_piece
                # selected_piece.set_position(new_row,new_col)
                if [new_col, new_row] in moves or [new_col, new_row] in attack_moves:
                    if (original_pos[0] != new_col or original_pos[1] != new_row):
                        # if(gb.preventer(original_pos,(new_col,new_row))):
                        gb.move(original_pos, (new_col, new_row))
                        move_id = selected_piece.get_identificator()[1] + letters[new_row] + str(8 - new_col)
                        history.append(move_id)
                        selected_piece.last_move = history[-1] if history else None
                        gb.curr_player = 'white' if gb.curr_player == 'black' else 'black'
                        gb.check_white = gb.check_black = False
                selected_piece = None
                moves, attack_moves = None, None
                mouse_down = False
        moves, attack_moves = None, None
        if selected_piece:
            moves, attack_moves = selected_piece.can_move(gb)
            moves, attack_moves = gb.preventer(moves, attack_moves, selected_piece)
            if type(selected_piece) == King:
                moves, attack_moves = gb.castle(moves, attack_moves, selected_piece)
        if mouse_down and selected_piece:
            x, y = pygame.mouse.get_pos()
            screen.blit(IMAGES[selected_piece.get_identificator()], (x - SIZE // 2, y - SIZE // 2))

        if mouse_down:
            draw_possible_moves(screen, moves, attack_moves)
            if gb.check_white or gb.check_black:
                show_checks(screen, gb)
        pygame.display.flip()

        # to not to get history printed too often
        # if fps_counter % 100 == 0:
        #     # print(history)
        #     # print(captured_pieces)
    pygame.quit()


if __name__ == "__main__":
    main()
