import pygame
from vars import *
import time

class GUI:
    def __init__(self):
        self.square_size = None


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
                    players, size = self.player_select_menu(screen)  # Call function to go to the next screen
                    self.square_size = int(min(width, height)/size)
                    return players, size
                    #waiting = False


    def player_select_menu(self, screen):
        """Displays the select players screen"""
        player_options = ['Human', 'Easy', 'Medium', 'Hard']
        size_board_options = ['5x5', '6x6', '7x7', '8x8']
        size='8x8'
        players = [None, None, "Human", "Human"]  # [player1, player2, difficulty1, difficulty2]
        screen.fill(GREY2)
        # Create a font object
        font = pygame.font.Font(None, 36)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # back player1
                    if 75 < event.pos[0] < 90 and 260 < event.pos[1] < 290:
                        players[2] = player_options[(player_options.index(players[2]) - 1) % len(player_options)]
                    # front player1
                    elif 210 < event.pos[0] < 225 and 260 < event.pos[1] < 290:
                        players[2] = player_options[(player_options.index(players[2]) + 1) % len(player_options)]

                    # back player2
                    if 325 < event.pos[0] < 340 and 260 < event.pos[1] < 290:
                        players[3] = player_options[(player_options.index(players[3]) - 1) % len(player_options)]
                    # front player2
                    elif 460 < event.pos[0] < 475 and 260 < event.pos[1] < 290:
                        players[3] = player_options[(player_options.index(players[3]) + 1) % len(player_options)]
                    
                    # decrease board size
                    elif 255 < event.pos[0] < 295 and 235 < event.pos[1] < 255:
                        size = size_board_options[(size_board_options.index(size) - 1) % len(size_board_options)]
                    # increase board size
                    elif 255 < event.pos[0] < 295 and 175 < event.pos[1] < 195:
                        size = size_board_options[(size_board_options.index(size) + 1) % len(size_board_options)]
                    
                    # START GAME!!
                    elif 250 < event.pos[0] < 300 and 335 < event.pos[1] < 365:
                        players[0] = 'Human' if players[2] == 'Human' else 'AI'
                        players[1] = 'Human' if players[3] == 'Human' else 'AI'

                        return players, int(size[0])

                    

            screen.fill(GREY2)  # Clear the screen

            #DameoGame_Name
            text_surface = font.render("Dameo Game", True, (50,50,50))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (200, 100)
            screen.blit(text_surface, text_rect)
            
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

            # Board_size
            text_surface = font.render("Board Size", True, (0,0,255))
            text_rect = text_surface.get_rect()
            text_rect.topright = (340, 150)
            screen.blit(text_surface, text_rect)

            # Box for player1
            pygame.draw.rect(screen, WHITE, (100, 250, 100, 50))
            pygame.draw.polygon(screen, BLACK, [(90, 260), (90, 290), (75, 275)])
            pygame.draw.polygon(screen, BLACK, [(210, 260), (210, 290), (225, 275)])
            text_surface = font.render(players[2], True, BLACK)
            text_rect = text_surface.get_rect()
            text_rect.center = (150, 275)
            screen.blit(text_surface, text_rect)

            # Box for player2
            pygame.draw.rect(screen, BLACK, (350, 250, 100, 50))
            pygame.draw.polygon(screen, WHITE, [(340, 260), (340, 290), (325, 275)])
            pygame.draw.polygon(screen, WHITE, [(460, 260), (460, 290), (475, 275)])
            text_surface = font.render(players[3], True, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.center = (400, 275)
            screen.blit(text_surface, text_rect)

            # Box for board_size
            pygame.draw.rect(screen, (180,165,100), (250, 200, 50, 30))
            pygame.draw.polygon(screen, GREY1, [(255, 195), (295, 195), (275, 175)])
            pygame.draw.polygon(screen, GREY1, [(255, 235), (295, 235), (275, 255)])
            text_surface = font.render(size, True, (0,0,255))
            text_rect = text_surface.get_rect()
            text_rect.center = (275, 215)
            screen.blit(text_surface, text_rect)

            # Box for start the game
            pygame.draw.rect(screen, (180,165,100), (250, 335, 50, 30))
            text_surface = font.render('GO!', True, (0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (275, 350)
            screen.blit(text_surface, text_rect)

            


            pygame.display.flip()
    
    def display_legal_moves(self, screen, legal_moves):
        """Highlight squares for legal moves"""
        for move in legal_moves:
            row, col = move
            pygame.draw.rect(screen, (180, 195, 100), (col * self.square_size, row * self.square_size, self.square_size, self.square_size))
            pygame.draw.rect(screen, (255, 255, 153), (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 3)
        
            
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
            pygame.draw.rect(screen, (50, 50, 50), (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 3)

    def display_message(self, screen, message, color=(135, 206, 250), place =(450, 190)):
        '''display message'''
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=place)
        screen.blit(text, text_rect)

    