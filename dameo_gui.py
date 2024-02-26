import pygame
from vars import *
import time

class GUI:
    def __init__(self):
        self.square_size = square_size


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
                    #self.player_select_menu(screen)  # Call function to go to the next screen
                    waiting = False

    def player_select_menu(self, screen):
        """Displays the select players screen"""
        players = [None, None, None, None]
        screen.fill(GREY2)
        # Create a font object
        font = pygame.font.Font(None, 36)

        # Player2
        text_surface = font.render("Player 1", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (100, 200)
        screen.blit(text_surface, text_rect)

        # Player1
        text_surface = font.render("Player 2", True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.topright = (450, 200)
        screen.blit(text_surface, text_rect)

        # Box for player1
        pygame.draw.rect(screen, WHITE, (100, 250, 100, 50))
        pygame.draw.polygon(screen, BLACK, [(90, 260), (90, 290), (75, 275)])
        pygame.draw.polygon(screen, BLACK, [(210, 260), (210, 290), (225, 275)])
        text_surface = font.render("Human", True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (150, 275)
        screen.blit(text_surface, text_rect)

        # Box for player2
        pygame.draw.rect(screen, BLACK, (350, 250, 100, 50))
        pygame.draw.polygon(screen, WHITE, [(340, 260), (340, 290), (325, 275)])
        pygame.draw.polygon(screen, WHITE, [(460, 260), (460, 290), (475, 275)])
        text_surface = font.render("Human", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (400, 275)
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        time.sleep(5)
    
    def display_legal_moves(self, screen, legal_moves):
        """Highlight squares for legal moves"""
        for move in legal_moves:
            row, col = move
            pygame.draw.rect(screen, (240, 120, 120), (col * square_size, row * square_size, square_size, square_size), 3)
            
            
    def display_turn(self, screen, turn):
        '''display who is the next to play'''
        font = pygame.font.Font(None, 28)
        text = font.render(f"{turn.capitalize()}", True,(135, 205, 250))
        text_rect = text.get_rect(center=(450, 50))
        screen.blit(text, text_rect)

    def display_selected_piece(self, screen, piece):
        '''highlight selected piece'''
        if piece:
            row, col = piece.row, piece.col
            pygame.draw.rect(screen, (50, 50, 50), (col * square_size, row * square_size, square_size, square_size), 3)

    def display_message(self, screen, message, color=(135, 206, 250), place =(450, 190)):
        '''display message'''
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=place)
        screen.blit(text, text_rect)

    