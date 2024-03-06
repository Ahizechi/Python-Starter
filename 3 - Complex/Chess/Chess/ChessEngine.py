
class GameState():

    def __init__(self):
        # Initializing the chess board with pieces, Row 1: Black Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook
        # Row 2: Black Pawns
        # Rows 3-6: Empty squares
        # Row 7: White Pawns
        # Row 8: White Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook
        self.board = [           
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", ],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP", ],      
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", ],
        ]
       
        # A flag to check whose turn it is, True if it's white's turn
        self.whiteToMove = True
        # A log to keep track of all the moves made in the game
        self.moveLog = []
        self.whiteKingLocation = [7, 4]
        self.blackKingLocation = [0, 4]
        self.inCheck = False
        self.pins = []
        self.checks = []
    
    # Does not work for pawn promo, castling and en passante
    def makeMove(self, move):
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.board[move.startRow][move.startColumn] = "--"
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endColumn)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endColumn)


    
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            self.board[move.endRow][move.endColumn] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.startRow, move.startColumn)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.startRow, move.startColumn)




    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:  # only 1 check, block check or move king
                moves = self.getAllPossibleMoves()  # to block a check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0]  # check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]  # enemy piece causing the check
                validSquares = []  # squares that pieces can move to
                # if knight, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]

                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)  # check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:  # once you get to piece end checks
                            break

                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # go through backwards when you are removing from a list as iterating
                    if moves[i].pieceMoved[1] != 'K':  # move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endColumn) in validSquares:  # move doesn't block check or capture piece
                            moves.remove(moves[i])

            else:  # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)

        else:  # not in check so all moves are fine
            moves = self.getAllPossibleMoves()

        return moves


    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                turn = self.board[row][column][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[row][column][1]
                    match piece:
                        case "P":
                            self.getPawnMoves(row, column, moves)
                        case "R":
                            self.getRookMoves(row, column, moves)
                        case "N":
                            self.getKnightMoves(row, column, moves)
                        case "B":
                            self.getBishopMoves(row, column, moves)
                        case "Q":
                            self.getQueenMoves(row, column, moves)
                        case "K":
                            self.getKingMoves(row, column, moves)
                        case _:
                            pass  # Do nothing for empty squares or unrecognized pieces
        return moves
    
    def getPawnMoves(self, row, column, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, - 1, - 1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break


        if self.whiteToMove:
            if self.board[row - 1][column] == "--":
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((row, column), (row - 1, column), self.board))
                    if row == 6 and self.board[row - 2][column] == "--":
                        moves.append(Move((row, column), (row - 2, column), self.board))
                
            if column - 1 >= 0: # Capture to the Left
                if self.board[row - 1][column - 1][0]:
                    if not piecePinned or pinDirection == (-1,-1):
                        moves.append(Move((row, column), (row - 1, column - 1), self.board))
            if column + 1 <= 7: # Capture to the Right
                if self.board[row - 1][column + 1][0]:
                    if not piecePinned or pinDirection == (-1,1):
                        moves.append(Move((row, column), (row - 1, column + 1), self.board))

        else: # Black pawn moves
            if self.board[row + 1][column] == "--": # Move forward
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((row, column), (row + 1, column), self.board))
                    if row == 1 and self.board[row + 2][column] == "--": # Double move from starting position
                        moves.append(Move((row, column), (row + 2, column), self.board))
            
            if column - 1 >= 0: # Capture to the Left
                if self.board[row + 1][column - 1][0] == 'w': # Check if there's a white piece to capture
                    if not piecePinned or pinDirection == (1,-1):
                        moves.append(Move((row, column), (row + 1, column - 1), self.board))
            if column + 1 <= 7: # Capture to the Right
                if self.board[row + 1][column + 1][0] == 'w': # Check if there's a white piece to capture
                    if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((row, column), (row + 1, column + 1), self.board))


    def getRookMoves(self, row, column, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][column][1] != 'Q':  # Can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Up, Left, Down, Right
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = column + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((row, column), (endRow, endCol), self.board))
                        elif endPiece[0] == enemy_color:
                            moves.append(Move((row, column), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break


    def getKnightMoves(self, row, column, moves):
        knightMoves = ((-2, 1), (-2, -1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2))
        ally_color = "w" if self.whiteToMove else "b"

        for m in knightMoves:
            endRow = row + m[0]
            endCol = column + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # On board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally_color:  # Not an ally piece (empty or enemy)
                    moves.append(Move((row, column), (endRow, endCol), self.board))



    def getBishopMoves(self, row, column, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))  # Diagonal directions
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = column + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((row, column), (endRow, endCol), self.board))
                        elif endPiece[0] == enemy_color:
                            moves.append(Move((row, column), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break




    def getQueenMoves(self, row, column, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))  # Diagonal directions
        enemy_color = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = column + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Empty space
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy_color:  # Enemy piece
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                        break
                    else:  # Friendly piece
                        break
                else:  # Off board
                    break


    def getKingMoves(self, r, c, moves):
        rowMoves = [-1, -1, -1, 0, 0, 1, 1, 1]
        colMoves = [-1, 0, 1, -1, 1, -1, 0, 1]
        allyColor = 'w' if self.whiteToMove else 'b'
        # Save the original king position to restore later
        originalKingPosition = self.whiteKingLocation if allyColor == 'w' else self.blackKingLocation
        
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # Empty square or contains enemy piece
                    # Move king temporarily to the new square
                    self.board[r][c] = "--"
                    self.board[endRow][endCol] = allyColor + 'K'
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    
                    # Undo temporary king move
                    self.board[r][c] = allyColor + 'K'
                    self.board[endRow][endCol] = endPiece
                    if allyColor == 'w':
                        self.whiteKingLocation = originalKingPosition
                    else:
                        self.blackKingLocation = originalKingPosition



    def checkForPinsAndChecks(self):
        pins = []  # squares where the allied pinned piece is and direction pinned from
        checks = []  # squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow, startCol = self.whiteKingLocation
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow, startCol = self.blackKingLocation

        # Directions to check for pins and checks
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
        for j in range(8):
            d = directions[j]
            possiblePin = ()  # reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():  # first allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:  # second allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # Conditions for possible checks
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():  # no blocking piece so it's a check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # blocking piece so it's a pin
                                pins.append(possiblePin)
                                break
                        else:  # enemy piece not applying check
                            break
                    else:  # empty square
                        continue
                else:  # off board
                    break

        # Check for knight checks
        knightMoves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':  # enemy knight attacking a king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks






class Move():
    
    # Maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startColumn = startSq[1]
        self.endRow = endSq [0]
        self.endColumn = endSq[1]
        self.pieceMoved = board[self.startRow][self.startColumn]
        self.pieceCaptured = board[self.endRow][self.endColumn]
        self.moveID =  self.startRow * 1000 + self.startColumn * 100 + self.endRow * 10 + self.endColumn
        # print(self.moveID)
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)
    
    def getRankFile(self, row, column):
        return self.colsToFiles[column] + self.rowsToRanks[row]
