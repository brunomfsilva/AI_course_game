import pygame

class GUI:

    def main_menu(self, screen):
        """Main Menu"""
        font = pygame.font.Font(None, 36)

        start_text = font.render("Click to Start", True, (255, 255, 255))  # select text and color
        text_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))  # Centre the text

        screen.fill((0, 0, 0))
        screen.blit(start_text, text_rect)
        pygame.display.flip()  # display

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # close if click on 'x' symbol
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Start if click on ecran
                    waiting = False

    def display_turn(self, screen, turn):
        '''display who is the next to play'''
        font = pygame.font.Font(None, 25)
        text = font.render(f"{turn.capitalize()}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(450, 50))
        screen.blit(text, text_rect)