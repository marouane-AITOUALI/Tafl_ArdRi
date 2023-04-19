import pygame
from .constants import SQUARE_SIZE, GRIS, CROWN, WHITE, BLACK, ROWS, COLS

class Piece:
    PADDING = 15
    BORDER = 2
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + (SQUARE_SIZE // 2)  
        self.y = SQUARE_SIZE * self.row + (SQUARE_SIZE // 2)
    
    def setKing(self):
        self.king = True
    
    def getRow(self):
        return self.row
    
    def getCol(self):
        return self.col
    
    def isKing(self):
        return self.king

    def make_king(self):
        self.king = True
    
    def draw(self, win):
        rayon = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GRIS, (self.x, self.y), rayon+self.BORDER) # Border du cercle 
        pygame.draw.circle(win, self.color, (self.x, self.y), rayon) # Remplissage de cercle

        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def verifyWinWhite(self):
        if self.color == WHITE and self.king:
            if (
                self.row == 0 and (self.col == 0 or self.col == COLS - 1)
                or self.row == ROWS - 1 and (self.col == 0 or self.col == COLS - 1)
                ):
                return True
        return False
    
    #def verifyWinBlack(self):


    def __repr__(self):
        return str(self.color)
    
    