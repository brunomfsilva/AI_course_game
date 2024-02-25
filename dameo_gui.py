import pygame
from vars import *

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
                    waiting = False
                    
    
    def display_legal_moves(self, screen, legal_moves):
        """Display legal moves as small blue dots"""
        for move in legal_moves:
            row, col = move
            pygame.draw.circle(screen, (0, 0, 255), (col * square_size + square_size // 2, row * square_size + square_size // 2), 5)
            #Fazer quadrado claro para as legal moves
            
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
            pygame.draw.rect(screen, (0, 0, 255), (col * square_size, row * square_size, square_size, square_size), 3)

    def display_message(self, screen, message, color=(135, 206, 250), place =(450, 190)):
        '''display message'''
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=place)
        screen.blit(text, text_rect)

    