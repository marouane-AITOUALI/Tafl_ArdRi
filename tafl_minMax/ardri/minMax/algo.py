from copy import deepcopy
from ..constants import BLACK, WHITE, COLS, ROWS
import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)


def miniMax2(position, depth, max_player, game, alpha,beta):
    if depth == 0 or position.getWinner() != None:          # Check if game is ended ??
        return position.evaluate(), position           # Checked and Changed in other functions...

    if max_player:
        bestMove = None
        for move in getAllMoves(position, WHITE, game):
            # move here is a board for getAllMoves
            evaluation = miniMax2(move, depth-1, False, game, alpha, beta)[0]
            if evaluation > alpha:
                alpha = evaluation
                bestMove = move
            if alpha >= beta:
                break
        return alpha, bestMove
    
    else:
        bestMove = None
        for move in getAllMoves(position, WHITE, game):
            # move here is a board for getAllMoves
            evaluation = miniMax2(move, depth-1, True, game, alpha, beta)[0]
            if evaluation < beta:
                beta = evaluation
                bestMove = move
            if beta <= alpha:
                break
        return beta, bestMove
    
    return 



def miniMax(position, depth, max_player, game):
    if depth == 0 or position.getWinner() != None:          # Check if game is ended ??
        return position.evaluate(), position            # Checked and Changed in other functions...

    if max_player:
        maxEvaluation = float('-inf')
        bestMove = None
        for move in getAllMoves(position, WHITE, game):
            # move here is a board for getAllMoves
            evaluation = miniMax(move, depth-1, False, game)[0]
            maxEvaluation = max(maxEvaluation, evaluation)
            if maxEvaluation == evaluation:
                bestMove = move
        return maxEvaluation, bestMove
    
    else:
        minEvaluation = float('inf')
        bestMove = None
        for move in getAllMoves(position, BLACK, game):
            # move here is a board for getAllMoves
            evaluation = miniMax(move, depth-1, True, game)[0]
            minEvaluation = min(minEvaluation, evaluation)
            if minEvaluation == evaluation:
                bestMove = move
        return minEvaluation, bestMove
    
    return 

def simulateMove(piece, row, col, board, game):
    board.move(piece, row, col)
    turn = game.getTurn()
    if(game.verifyWhiteWin()):
                game.run = False
                game.board.setWinner(WHITE)
                # WHITE WIN
                
            
    if row - 1 >= 0 and board.board[row-1][col] != 0 and board.board[row-1][col].color != turn:
        if (board.board[row-1][col].king):
            result = board.verifyKingCaptured(board.board[row-1][col])
            if result:
                board.setWinner(BLACK)
                # KING WIN
                
        else:
            board.verifyPionCaptured(board.board[row-1][col])
    
    if row + 1 < ROWS and board.board[row+1][col] != 0 and board.board[row+1][col].color != turn:
        if(board.board[row+1][col].king):
            result = board.verifyKingCaptured(board.board[row+1][col])
            if result:
                board.setWinner(BLACK)
                # KING WIN
                
        else:
            board.verifyPionCaptured(board.board[row+1][col])
    
    if col + 1 < COLS and board.board[row][col + 1] != 0 and board.board[row][col+1].color != turn:
        if(board.board[row][col+1].king):
            result = board.verifyKingCaptured(board.board[row][col+1])
            if result:
                board.setWinner(BLACK)
                # KING WIN
                
        else:
            board.verifyPionCaptured(board.board[row][col+1])
    
    if col - 1 >= 0 and board.board[row][col-1] != 0 and board.board[row][col-1].color != turn:
        if(board.board[row][col-1].king):
            result = board.verifyKingCaptured(board.board[row][col-1])
            if result:
                board.setWinner(BLACK)
                # KING WIN
                
        else:
            board.verifyPionCaptured(board.board[row][col-1])
    
    return board

# Return all Board possible for every move of color=color
def getAllMoves(board, color, game):
    moves = []

    for piece in board.getAllPieces(color):
        validMoves = board.getValidMoves(piece)
        for row, col in validMoves:
            tempBoard = deepcopy(board)
            tempPiece = tempBoard.getPiece(piece.getRow(), piece.getCol())
            newBoard = simulateMove(tempPiece, row, col, tempBoard, game)
            moves.append(newBoard)

    return moves
