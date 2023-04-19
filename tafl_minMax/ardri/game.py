import pygame
from .board import Board
from .constants import BLACK, WHITE, BLUE, SQUARE_SIZE, ROWS, COLS

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.drawValidMoves(self.validMoves)
        pygame.display.update()
    
    def _init(self):
        self.selected = None
        self.run = True
        self.board = Board()
        self.turn = BLACK
        self.validMoves = []
    
    def reset(self):
        self._init()

    def getRun(self):
        return self.run
    
    def setRun(self, bool):
        self.run = bool
    
    def getTurn(self):
        return self.turn
    
    def select(self, row, col):
        
        if self.selected:
            result = self._move(row,col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.getPiece(row, col)
        
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.validMoves = self.board.getValidMoves(piece)

            # Must implement method for the valid moves !!
            #self.validMoves = self.board.getValidMoves(piece)
            
            return True
        
        return False


    def verifyWhiteWin(self):
        if (
            self.board.board[0][0] != 0 and self.board.board[0][0].isKing()
            or self.board.board[0][COLS-1] != 0 and self.board.board[0][COLS-1].isKing()
            or self.board.board[ROWS-1][0] != 0 and self.board.board[ROWS-1][0].isKing()
            or self.board.board[ROWS-1][COLS-1] != 0 and self.board.board[ROWS-1][COLS-1].isKing()
            or self.board.getBlackLeft() == 0):
            self.board.setWinner(BLACK)
            return True
        return False

    def _move(self, row, col):
        piece = self.board.getPiece(row, col)
        if self.selected and piece == 0  and ((row, col) in self.validMoves):
            self.board.move(self.selected, row, col)

            # Delete ..??
            if(self.verifyWhiteWin()):
                self.run = False
                self.board.setWinner(WHITE)
                print("White's Victory")
                
            
            if row - 1 >= 0 and self.board.board[row-1][col] != 0 and self.board.board[row-1][col].color != self.turn:
                if (self.board.board[row-1][col].king):
                    result = self.board.verifyKingCaptured(self.board.board[row-1][col])
                    if result:
                        self.run = False
                        self.board.setWinner(BLACK)
                        print("King's Captured ! Black Pions Wins")
                        
                else:
                    self.board.verifyPionCaptured(self.board.board[row-1][col])
            
            if row + 1 < ROWS and self.board.board[row+1][col] != 0 and self.board.board[row+1][col].color != self.turn:
                if(self.board.board[row+1][col].king):
                    result = self.board.verifyKingCaptured(self.board.board[row+1][col])
                    if result:
                        self.run = False
                        self.board.setWinner(BLACK)
                        print("King's Captured ! Black Pions Wins")
                        
                else:
                    self.board.verifyPionCaptured(self.board.board[row+1][col])
            
            if col + 1 < COLS and self.board.board[row][col + 1] != 0 and self.board.board[row][col+1].color != self.turn:
                if(self.board.board[row][col+1].king):
                    result = self.board.verifyKingCaptured(self.board.board[row][col+1])
                    if result:
                        self.run = False
                        self.board.setWinner(BLACK)
                        print("King's Captured ! Black Pions Wins")
                        
                else:
                    self.board.verifyPionCaptured(self.board.board[row][col+1])
            
            if col - 1 >= 0 and self.board.board[row][col-1] != 0 and self.board.board[row][col-1].color != self.turn:
                if(self.board.board[row][col-1].king):
                    result = self.board.verifyKingCaptured(self.board.board[row][col-1])
                    if result:
                        self.run = False
                        self.board.setWinner(BLACK)
                        print("King's Captured ! Black Pions Wins")
                        
                else:
                    self.board.verifyPionCaptured(self.board.board[row][col-1])
                    
            
            self.change_turn()
        else:
            return False
        return True
    
    def drawValidMoves(self, moves):
        for r, c in moves:
            row, col = r, c
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)
        
    def change_turn(self):
        self.validMoves = []
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def getBoard(self):
        return self.board

    def aiMove(self, board):
        self.board = board
        self.change_turn()

