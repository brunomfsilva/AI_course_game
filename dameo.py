import pygame
import utils

def main():
    """Initiate game"""

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

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
        utils.draw_chessboard(screen, square_size, WHITE, BLACK)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()