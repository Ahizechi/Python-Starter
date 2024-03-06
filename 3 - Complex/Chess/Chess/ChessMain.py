import pygame as pg
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "bP", "wP"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("Chess/Images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = ChessEngine.GameState()
    
    validMoves = gs.getValidMoves()

    moveMade = False # Flag variable for when a move is made

    loadImages()
    running = True
    sqSelected = () # Keeps track of last click of the user (one tuple)
    playerClicks = [] # Keeps track of player clicks (two tuples)
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                column = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, column):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, column)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print("Attempting move:", move.getChessNotation())
                    
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        print("Move made:", move.getChessNotation())
                        sqSelected = ()
                        playerClicks = []

                    else:
                        print("Invalid move:", move.getChessNotation())
                        playerClicks = [sqSelected]


            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_u: # undo when U is pressed
                    gs.undoMove()
                    moveMade = True
        
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            # print("New valid moves:", [mv.getChessNotation() for mv in validMoves])

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pg.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [pg.Color("white"), pg.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[(row+column) % 2]
            pg.draw.rect(screen, color, pg.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()