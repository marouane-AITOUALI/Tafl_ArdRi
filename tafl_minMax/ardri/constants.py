import pygame 

WIDTH, HEIGHT = 700, 700
ROWS, COLS = 7, 7
SQUARE_SIZE = WIDTH//COLS


ALPHA = float('-inf')
BETA = float('inf')

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)

BOARD_COLOR = (63,255,102)

GRIS = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))