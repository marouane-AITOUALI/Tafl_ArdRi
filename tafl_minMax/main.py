import pygame
from ardri.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, WHITE, ALPHA, BETA
from ardri.game import Game
from ardri.minMax.algo import miniMax, miniMax2

FPS = 60

# THE GAME WINDOW
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ard-ri")


def getRowColFromMouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE

    return row, col


def main():
    # Speed of the game
    clock = pygame.time.Clock()
    game = Game(WIN)
    


    while(game.getRun()):
        clock.tick(FPS)

        if game.turn == WHITE:
            value, newBoard = miniMax2(game.getBoard(), 3, WHITE, game, ALPHA, BETA)
            print("La valeur pour ce mouvement: ", value)
            
            game.aiMove(newBoard)
            if game.verifyWhiteWin():
                print("White's Victory !!")
                game.setRun(False) 
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = getRowColFromMouse(pos)
                #if game.turn == BLACK: # White is for AI
                game.select(row, col)


        game.update()
        

    pygame.quit()
        


main()