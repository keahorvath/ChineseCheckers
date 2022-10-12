import random

class GameSetup:
    """Class which contains all the information about the game setup
    (what the player chose)"""

    def __init__(self):
        """Class initializer"""
        self.classicMode = "CLASSIC MODE"
        self.fastPacedMode = "FAST-PACED MODE"
        self.easy = "EASY"
        self.normal = "NORMAL"
        self.hard = "HARD"
        self.gameMode = self.classicMode
        self.difficultyAI = None
        self.gameAgainstAI = False
        self.playerNames = ["", ""]
        self.playerColors = []


class GameState:
    """Class which contains all the information about the current state of the game,
    and the functions needed to make the game work"""

    def __init__(self, gameSetup):
        """Class initializer"""
        self.gameSetup = gameSetup

        self.grid = [ [None]*17 for i in range(25)] #Creates a 25 by 17 grid
        self.score = [0, 0]
        if self.gameSetup.gameAgainstAI :
            self.currentPlayer = 1
        else:
            self.currentPlayer = random.randint(1,2) #The player that starts is chosen at random
        self.winner = None

        self.selectedMarble = None
        self.allowedMoves = []
        self.beginningCell = [None]
        self.nbMovesInTurn = 0

        self.totalNbTurns = [0, 0]
        self.nbSimpleMoves = [0, 0]
        self.totalNbJumps = [0, 0]
        self.previousMove = [None, None] #The previous move was from the element of index 0 to the element of index 1
        self.previousNbSimpleMoves = [0, 0]#Used when the undo button is pressed
        self.previousTotalNbJumps = [0, 0]

        self.makeListCellsInTriangles()
        self.initializeGrid()

    def initializeGrid(self):
        """This function creates the "star" shape by asigning the right value to each cell in the grid
        (see developer doc part 3.1)"""

        #Step 1: All the cells that are inside of the star get the value 0
        nb_of_cells = 1
        mvt = 'more'
        for line in range(17):
            self.grid[12][line] = 0
            if line == 4:
                mvt = 'less'
                nb_of_cells = 25
            if line == 8:
                mvt = 'more'
            if line == 13:
                mvt = 'less'
                nb_of_cells = 7
            for j in range(1, (nb_of_cells+1)//2):
                self.grid[12-j][line] = 0
                self.grid[12+j][line] = 0
            if mvt == 'more':
                nb_of_cells += 2
            else:
                nb_of_cells -= 2

        #Step 2: Even lines only have cells with even columns and odd lines only have cells with odd columns
        for j in range(17):
            for i in range(25):
                if (i%2 == 0 and j%2 != 0) or (i%2 != 0 and j%2 == 0):
                    self.grid[i][j] = None

        #Step 3: At the beginning of the game, the bottom "triangle" contains all the player 1 marbles
        #and the top "triangle" contains all the player 2 marbles
        for j in range(13, 17):
            for i in range(9, 17):
                if self.getCell(i, j) == 0:
                    self.grid[i][j] = 1
        for j in range(0, 4):
            for i in range(9, 17):
                if self.getCell(i, j) == 0:
                    self.grid[i][j] = 2

    def makeListCellsInTriangles (self):
        """This function creates a list containing all the cells that are in the 4 side triangles"""
        self.listCellsInTriangles = []
        listCellsInTopLeftTriangle = [(0, 4), (2, 4), (4, 4), (6, 4), (1, 5), (3, 5), (5, 5), (2, 6), (4, 6), (3, 7)]
        for i in listCellsInTopLeftTriangle:
            self.listCellsInTriangles += [i, (24 - i[0], i[1]), (i[0], 16 - i[1]), (24 - i[0], 16 - i[1])]

    def resetVariables(self):
        """This function is called when the game is restarted and resets the necessary variables"""
        self.winner = None
        self.totalNbTurns = [0, 0]
        self.nbSimpleMoves = [0, 0]
        self.totalNbJumps = [0, 0]
        self.selectedMarble = None
        self.allowedMoves = []

    def play(self, x, y):
        """This function is called when a player clicks and determines what should be done"""
        if not (self.gameSetup.gameAgainstAI and self.currentPlayer == 2):
            self.previousNbSimpleMoves = self.nbSimpleMoves[:]
            self.previousTotalNbJumps = self.totalNbJumps[:]

        if self.selectedMarble == (x, y) and self.nbMovesInTurn != 0:
            #If the player clicks on his selectedMarble and he has already done some moves in his turn,
            #his turn is over and all the necessary variables are reset
            if self.selectedMarble not in self.listCellsInTriangles:
                if (self.gameSetup.gameAgainstAI and self.currentPlayer == 2):
                    self.previousMove = [(self.previousMove[0]), (self.previousMove[1]),(self.beginningCell) ,(self.selectedMarble)]
                else:
                    self.previousMove = [(self.beginningCell) ,(self.selectedMarble)]
                self.selectedMarble = None
                self.allowedMoves = []
                self.totalNbJumps[self.currentPlayer - 1] += self.nbMovesInTurn
                self.totalNbTurns[self.currentPlayer - 1] += 1
                self.currentPlayer = 3 - self.currentPlayer
                self.nbMovesInTurn = 0

                return "turn is over"

        elif self.grid[x][y] == self.currentPlayer and self.nbMovesInTurn == 0:
            #If the player clicks on a marble that is his, and he hasn't moved a marble yet,
            #The clicked marble becomes the new selectedMarble and we make a new list with his allowed moves
            self.selectedMarble = (x, y)
            self.allowedMoves = self.makeListOfAllowedMoves(x, y)
            self.beginningCell = (x, y) #Is used in case of an undo
            return None

        elif self.grid[x][y] == 0 and self.selectedMarble is not None and self.moveIsAllowed(x, y):
            #If the player clicks on a "hole" and he has already selected the marble to move and the move is valid,
            #The selected marble becomes a hole and his marble is moved to the chosen cell

            self.grid[self.selectedMarble[0]][self.selectedMarble[1]] = 0
            self.grid[x][y] = self.currentPlayer
            if self.moveIsSimple(self.selectedMarble, (x, y)):
                #If the move that just occured is a simple move(no jumping)
                #then the variables are reset and the turn is over (goes to other player)
                if (self.gameSetup.gameAgainstAI and self.currentPlayer == 2):
                    self.previousMove = [(self.previousMove[0]), (self.previousMove[1]), (self.beginningCell) ,(x, y)]
                else:
                    self.previousMove = [(self.beginningCell) ,(x, y)]
                self.selectedMarble = None
                #STATS:
                self.nbSimpleMoves[self.currentPlayer - 1] += 1
                self.totalNbTurns[self.currentPlayer - 1] += 1

                self.currentPlayer = 3 - self.currentPlayer
                self.nbMovesInTurn = 0
                self.allowedMoves = []

                return "turn is over"

            #Else (the move was a jump),
            #The new position becomes the selectedMarble and the list of allowed moves is made
            self.selectedMarble = (x, y)
            self.nbMovesInTurn += 1
            self.allowedMoves = self.makeListOfAllowedMoves(x, y)
            if self.beginningCell == (x, y):
                self.nbMovesInTurn = 0

        return None

    def getCell(self, x, y):
        """This function gives the value of a cell, being given the row and column"""
        if x < 25 and x >= 0 and y < 17 and y >= 0:
            return self.grid[x][y]

    def isGameOver(self):
        """This function determines if the game is over """
        #These are all the positions that the player's marble should be in in order to win
        player1_win_cells_y = [0, 1, 1, 2, 2, 2, 3, 3, 3, 3]
        player2_win_cells_y = [16, 15, 15, 14, 14, 14, 13, 13, 13, 13]
        players_win_cells_x = [12, 11, 13, 10, 12, 14, 9, 11, 13, 15]

        #Checks if all the marbles are in the winning position
        if all(self.grid[players_win_cells_x[i]][player1_win_cells_y[i]] == 1 for i in range (len(players_win_cells_x))):
            return True
        elif all(self.grid[players_win_cells_x[i]][player2_win_cells_y[i]] == 2 for i in range (len(players_win_cells_x))):
            return True
        return False

    def makeListOfAllowedMoves(self, x, y):
        """This function makes a list of all the moves a player is allowed to make from a certain position"""
        allowedMoves = []
        #First we check all of the cells that are around the selected cell
        if self.nbMovesInTurn == 0:
            for i in range (6):
                aroundCell = self.getAroundCell(x, y, 1, i)
                if self.getCell(*aroundCell) == 0 and aroundCell not in self.listCellsInTriangles:
                    #First we add to the list of allowed cells all of the empty cells that are allowed(not in side triangles)
                    allowedMoves += [aroundCell]

        if self.gameSetup.gameMode == "CLASSIC MODE":
            for i in range (6):
                #We look in all the directions
                dist = 1
                aroundCell = self.getAroundCell(x, y, 1, i)

                if self.getCell(*aroundCell) == 1 or self.getCell(*aroundCell) == 2:
                    #If the adjacent cell contains a marble
                    nextCell = self.getAroundCell(x, y, 2, i)
                    if self.getCell(*nextCell) == 0:
                        #If the cell behind this one is empty, we can place the marble there
                        allowedMoves += [nextCell]

        if self.gameSetup.gameMode == "FAST-PACED MODE":
            for i in range (6):
                #We look in all the directions
                dist = 1
                currentCell = self.getAroundCell(x, y, dist, i)

                while self.getCell(*currentCell) != 1 and self.getCell(*currentCell) != 2 and self.getCell(*currentCell) is not None:
                    #While the current cell doesn't have a marble or doesn't go out of the grid
                    dist += 1
                    currentCell = self.getAroundCell(x, y, dist, i)

                if self.getCell(*currentCell) is None:
                    continue

                for j in range (1, dist + 1):
                    #We now look if we can place a marble on that line such that the distance separating the found marble
                    #is the same as the distance separating the original cell and the found marble
                    nextCell = self.getAroundCell(x, y, dist + j, i)

                    if self.getCell(*nextCell) != 0:
                        #If before getting to the right cell, a cell isn't empty, we move to the next direction
                        break

                    if j == dist:
                        #If we get to the right cell, it is a possible position
                        allowedMoves += [nextCell]

        return allowedMoves

    def getAroundCell(self, x, y, d, ind):
        """This function returns a list with the 6 cells that are around the (x, y) cell"""
        aroundCells = [(x-d, y-d), (x+d, y-d), (x+2*d, y), (x+d, y+d), (x-d, y+d), (x-2*d, y)]
        return aroundCells[ind]

    def moveIsAllowed(self, new_x, new_y):
        """This function checks if you can go from the current position to the new position"""
        if (new_x, new_y) in self.allowedMoves:
            return True
        return False

    def moveIsSimple(self, originalCell, newCell):
        """Checks if the move from the original cell to the new cell is simple"""
        for i in range(6):
            if self.getAroundCell(*originalCell, 1, i) == newCell:
                return True
        return False
