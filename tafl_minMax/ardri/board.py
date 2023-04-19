import pygame
from .constants import BOARD_COLOR, SQUARE_SIZE, BLACK, RED, ROWS, COLS, WHITE, ROWS, COLS
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.white_left = 9
        self.black_left = 16
        self.winner = None
        self.create_board()

    def drawBoard(self, win):
        win.fill(BOARD_COLOR)
        for row in range(2,5):
            for cols in range(2,5):
                pygame.draw.rect(win, BLACK, (row*SQUARE_SIZE, cols*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        pygame.draw.rect(win, RED, (3*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(win, RED, (SQUARE_SIZE, 3*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(win, RED, (5*SQUARE_SIZE, 3*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(win, RED, (3*SQUARE_SIZE, 5*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for i in range (2,5):
            pygame.draw.rect(win, RED, (i*SQUARE_SIZE, 0, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(win, RED, (0, i*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(win, RED, (i*SQUARE_SIZE, 6*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(win, RED, (6*SQUARE_SIZE, i*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def getWinner(self):
        if self.winner != None:
            return self.winner
        return None

    def getWhiteLeft(self):
        return self.white_left

    def getBlackLeft(self):
        return self.black_left

    def setWinner(self, color):
        self.winner = color

    def getPiece(self, row, col):
        return self.board[row][col]

    def getAllPieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def getKing(self):
        pieces = self.getAllPieces(WHITE)
        for piece in pieces:
            if piece.isKing():
                return piece
    
    def create_board(self):
        for row in range(ROWS):
            self.board.append([0,0,0,0,0,0,0])
        # Les assaillants
        for i in range(2,5):
            self.board[0][i]= Piece(0,i,BLACK)
            self.board[i][0] = Piece(i,0,BLACK)

            self.board[i][6] = Piece(i,6,BLACK)
            self.board[6][i] = Piece(6,i,BLACK)
        
        self.board[1][3] = Piece(1,3,BLACK)
        self.board[3][1] = Piece(3,1,BLACK)
        self.board[3][5] = Piece(3,5,BLACK)
        self.board[5][3] = Piece(5,3,BLACK)

        # Les BLancs
        for i in range(2,5):
            for j in range(2,5):
                    piece = Piece(i,j,WHITE)
                    if i == 3 and j == 3:
                        piece.setKing()
                    self.board[i][j] = piece

        #for i in range(7):
         #   for j in range(7):
          #      print(self.board[i][j])


    def draw(self, win):
        self.drawBoard(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    
    def evaluate(self):
        king = self.getKing()
        distance = self.getDistanceForWin(king)
        # On evalue par rapport à la distance au coin pour gagner
        # La distance maximale que le roi peut s'éloigner (en prenant en considération les 4 forteresses coins) est 6
        res = (6-distance)*100
        if (self.winner != None and self.winner == WHITE):
            res += 1000
        if(self.winner != None and self.winner == BLACK):
            res -= 1000
        return (res + (self.white_left - self.black_left)) * (1/(1+distance))

    def getDistanceForWin(self, king):
        distances = []
        row = king.getRow()
        col = king.getCol()
        winPos = [(0,0), (0, COLS-1), (ROWS-1, 0), (ROWS-1, COLS-1)]
        for x2, y2 in winPos:
            distances.append(self.calcDistance(row,col,x2,y2))
        
        return min(distances)
    
    # MANHATTAN DISTANCE
    def calcDistance(self, x1, y1, x2, y2):
        return abs(x1-x2) + abs(y1-y2)

    def move(self, piece, row, col):
        if (piece != 0 and self.board[row][col] == 0):
            self.board[piece.getRow()][piece.getCol()], self.board[row][col] = self.board[row][col], self.board[piece.getRow()][piece.getCol()]
            piece.move(row,col)


    def getValidMoves(self, piece):
        moves = []
        row = piece.row
        col = piece.col

        # Left validMoves
        for i in range(col-1, -1, -1):
            if self.board[row][i] == 0:
                moves.append((row,i))
            else:
                break
        
        # Right validMoves
        for i in range(col+1, COLS):
            if self.board[row][i] == 0:
                moves.append((row,i))
            else:
                break
        
        # Bot validMoves
        for i in range(row+1, ROWS):
            if self.board[i][col] == 0:
                moves.append((i,col))
            else:
                break

        # TOP validMoves
        for i in range(row-1, -1,-1):
            if self.board[i][col] == 0:
                moves.append((i,col))
            else:
                break
        
        # Filtrer les mouvements interdits pour les assaillants
        if (piece.color == BLACK):
            moves = [m for m in moves if m != (0,0)
                     and m != (0, COLS-1) and m != (ROWS - 1, 0)
                     and m != (ROWS - 1, COLS-1) and m != (3,3)
                     ]
            #moves.remove([0,0], [0, COLS-1], [ROWS - 1, 0], [ROWS - 1, COLS-1])

        return moves
    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
        

    def reduceOne(self, color):
        if color == BLACK:
            self.black_left -= 1
        else:
            self.white_left -= 1

    def verifyPionCaptured(self, piece):
        row = piece.row
        col = piece.col
        color = piece.color
        isRemoved = False

        # Check Horizontally 
        if (col + 1 < COLS and self.board[row][col+1] != 0 and self.board[row][col+1].color != color):
            if(col - 1 >= 0 and self.board[row][col-1] != 0 and self.board[row][col-1].color != color
               or col - 1 == 0 and (row == 0 or row == ROWS - 1)
               or row - 1 >= 0 and self.board[row-1][col] != 0 and self.board[row - 1][col].color != color
               or row + 1 < ROWS and self.board[row+1][col] != 0 and self.board[row + 1][col].color != color):
                self.board[row][col] = 0
                isRemoved = True
        
        if (col - 1 >= 0 and self.board[row][col -1] != 0 and self.board[row][col -1].color != color):
            if (col + 1 == COLS - 1 and (row == 0 or row == ROWS - 1)
                or row - 1 >= 0 and self.board[row-1][col] != 0 and self.board[row - 1][col].color != color
                or row + 1 < ROWS and self.board[row+1][col] != 0 and self.board[row + 1][col].color != color):
                self.board[row][col] = 0
                isRemoved = True
        
        # Check Vertically

        if (row + 1 < ROWS and self.board[row+1][col] != 0 and self.board[row+1][col].color != color):
            if (row - 1 >= 0 and self.board[row-1][col] != 0 and self.board[row-1][col].color != color
                or row - 1 == 0 and (col == 0 or col == COLS - 1)
                or col - 1 >= 0 and self.board[row][col-1] != 0 and self.board[row][col-1].color != color
                or col + 1 < COLS and self.board[row][col+1] != 0 and self.board[row][col+1].color != color):

                self.board[row][col] = 0
                isRemoved = True

        if (row - 1 >= 0 and self.board[row-1][col] != 0 and self.board[row - 1][col].color != color):
            if (row + 1 < ROWS and self.board[row+1][col] != 0 and self.board[row+1][col].color != color
                or row + 1 == ROWS - 1 and (col == 0 or col == COLS - 1)):
                self.board[row][col] = 0
                isRemoved = True
        
        if isRemoved:
            self.reduceOne(color)
        
        

    

    def verifyKingCaptured(self, piece):
        row = piece.row
        col = piece.col

        # Verify king is surrounded
        if(col - 1 >= 0 and self.board[row][col - 1] != 0 and self.board[row][col - 1].color == BLACK):
            if(col + 1 < COLS and self.board[row][col+1] != 0 and self.board[row][col+1].color == BLACK):
                if(row - 1 >=0 and self.board[row-1][col] != 0 and self.board[row-1][col].color == BLACK):
                    if(row + 1 < ROWS and self.board[row+1][col] != 0 and self.board[row+1][col].color == BLACK):
                        return True
        
        # Verify Edges
            
        if (col-1 >= 0 and self.board[row][col - 1] != 0 and self.board[row][col - 1].color == BLACK):
            if(col + 1 < COLS and self.board[row][col+1] != 0 and self.board[row][col+1].color == BLACK):
                #TOP EDGE
                if(row + 1 < ROWS and self.board[row+1][col] != 0 and self.board[row+1][col].color == BLACK and row == 0):
                    return True
                #BOT EDGE
                if (row - 1 >=0 and self.board[row-1][col] != 0 and self.board[row-1][col].color == BLACK and row == ROWS - 1):
                    return True

        
        if(row - 1 >=0 and self.board[row-1][col] != 0 and self.board[row-1][col].color == BLACK):
            if(row + 1 < ROWS and self.board[row+1][col] != 0 and self.board[row+1][col].color == BLACK):
                #LEFT EDGE
                if(col + 1 < COLS and self.board[row][col+1] != 0 and self.board[row][col+1].color == BLACK and col == 0):
                    return True
                #RIGHT EDGE
                if(col-1 >= 0 and self.board[row][col - 1] != 0 and self.board[row][col - 1].color == BLACK and col == COLS - 1):
                    return True
        
        # TOP      
        if(row -1 == 0):
            #LEFT FORTERESSE
            if(col ==0):
                if(col+1 < COLS and self.board[row][col+1] != 0 and self.board[row][col+1].color == BLACK):
                    if(row + 1 < ROWS and self.board[row+1][col] != 0 and self.board[row+1][col].color == BLACK):
                        return True
            
            #RIGHT FORTERESSE
            if (col == COLS -1):
                if (col -1 >= 0 and self.board[row][col - 1] != 0 and self.board[row][col - 1].color == BLACK):
                    if(row + 1 < ROWS and self.board[row+1][col] != 0 and self.board[row+1][col].color == BLACK):
                        return True
                    
        # BOTTOM
        if(row +1 == ROWS - 1):
            # LEFT FORTERESSE
            if(col == 0):
                if(row - 1 >=0 and self.board[row-1][col] != 0 and self.board[row-1][col].color == BLACK):
                    if(col + 1 < COLS and self.board[row][col+1] != 0 and self.board[row][col+1].color == BLACK):
                        return True
            
            # RIGHT FORTERESSE
            if(col == COLS - 1):
                if (row - 1 >=0 and self.board[row-1][col] != 0 and self.board[row-1][col].color == BLACK):
                    if (col -1 >= 0 and self.board[row][col - 1] != 0 and self.board[row][col - 1].color == BLACK):
                        return True
        
        # CENTER
            # LEFT
        if (col -1 == 3 and row == 3):
            if(self.board[row-1][col] != 0 and self.board[row-1][col].color == BLACK
               and self.board[row+1][col] != 0 and self.board[row+1][col].color == BLACK
               and self.board[row][col+1] != 0 and self.board[row][col+1].color == BLACK):
                return True
                
            # RIGHT
        if (col + 1 == 3 and row == 3):
            if(self.board[row-1][col] != 0 and self.board[row-1][col].color == BLACK
               and self.board[row+1][col] != 0 and self.board[row+1][col].color == BLACK
               and self.board[row][col-1] != 0 and self.board[row][col-1].color == BLACK):
                return True
            # TOP
        if (row - 1 == 3 and col == 3):
            if(self.board[row][col+1] != 0 and self.board[row][col+1].color == BLACK
               and self.board[row][col-1] != 0 and self.board[row][col-1].color == BLACK
               and self.board[row+1][col] != 0 and self.board[row+1][col].color == BLACK):
                return True
            # BOTTOM
        if(row + 1 == 3 and col == 3):
            if(self.board[row][col+1] != 0 and self.board[row][col+1].color == BLACK
               and self.board[row][col-1] != 0 and self.board[row][col-1].color == BLACK
               and self.board[row-1][col] != 0 and self.board[row-1][col].color == BLACK):
                return True
        
        # FORTERESSE IS AT RIGHT
            
        if (col + 1 == COLS - 1 and (row == 0 or row == ROWS - 1)):
            if (col -1 >= 0 and self.board[row][col - 1] != 0 and self.board[row][col - 1].color == BLACK):
                if(row - 1 >=0 and self.board[row-1][col] != 0 and self.board[row-1][col].color == BLACK
                   or row + 1 < ROWS and self.board[row+1][col] != 0 and self.board[row+1][col].color == BLACK):
                    return True
            
        # FORTERESSE IS AT LEFT

        if (col - 1 == 0 and (row == 0 or row == ROWS - 1)):
            if(col + 1 < COLS and self.board[row][col + 1] != 0 and self.board[row][col + 1].color == BLACK):
                if(row - 1 >=0 and self.board[row-1][col] != 0 and self.board[row-1][col].color == BLACK
                   or row + 1 < ROWS and self.board[row+1][col] != 0 and self.board[row+1][col].color == BLACK):
                    return True
        

        # FORTERESSE IS AT TOP
        if(row - 1 == 0 and (col == 0 or col == COLS - 1)):
            if(self.board[row+1][col] != 0 and self.board[row+1][col].color == BLACK):
                if(
                    self.board[row][col + 1] != 0 and self.board[row][col + 1].color == BLACK
                    or self.board[row][col - 1] != 0 and self.board[row][col - 1].color == BLACK
                ): return True

        # FORTERESSE IS AT BOTTOM
        if (row + 1 == ROWS - 1 and (col == 0 or col == COLS - 1)):
            if(self.board[row-1][col] != 0 and self.board[row-1][col].color == BLACK):
                if(
                   self.board[row][col + 1] != 0 and self.board[row][col + 1].color == BLACK
                    or self.board[row][col - 1] != 0 and self.board[row][col - 1].color == BLACK
                ): return True








        
        
        


            


        