import pygame
import utils
from board import Board
import piece

def main():
    """Initiate game"""

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREY1 = (200, 200, 200)
    GREY2 = (50, 50, 50)

    pygame.init()
    square_size = 50
    width = 8 * square_size
    height = 8 * square_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('DAMEO')
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0,0,0))
        utils.draw_chessboard(screen, square_size, GREY1, GREY2)
        pygame.display.flip()

        for i in range(18):
            utils.draw_piece(screen, piece.all_pieces_black[i].row, piece.all_pieces_black[i].col, square_size, piece.all_pieces_black[i])
            utils.draw_piece(screen, piece.all_pieces_white[i].row, piece.all_pieces_white[i].col, square_size, piece.all_pieces_white[i])
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()