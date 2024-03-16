import pygame
import Utils.Map as mp

WIDTH, HEIGHT = 800, 800
ROW, COLUMN = 8, 8
SIZE = WIDTH // ROW
IMAGES = {}
# Define colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

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


def main():
    pygame.init()
    pygame.font.init()
    load_images()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    gb = mp.Map(8, 8)
    board = gb.board

    pygame.display.set_caption("Chess")
    timer = pygame.time.Clock()
    running = True
    while running:
        timer.tick(fps)
        draw_board(screen)
        draw_pieces(screen, board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
