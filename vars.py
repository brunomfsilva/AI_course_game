import pygame

pygame.init() 

WHITE = (255, 253, 208)
BLACK = (200, 42, 42)
GREY1 = (100, 100, 100)
GREY2 = (128, 180, 180)

width, height = 550, 400


efeito_w = pygame.mixer.Sound("sounds\winner.mp3")
efeito_k = pygame.mixer.Sound("sounds\king_sound.mp3")