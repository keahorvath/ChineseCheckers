import random

class AI:
    """Class that contains all the information and functions regarding the AI"""

    def __init__(self, gameState):
        """Class initializer"""
        self.marblesPos = []
        for i in range(25):
            for j in range(17):
                if gameState.getCell(i, j) == 2:
                    self.marblesPos += [(i, j)]
        self.allPossibleMoves = []
        self.points = []

    def moveAI(self, gameState):
        """Function called in Game class
        Determines what needs to be done to make AI play
        Returns the chosen move for the AI
        """
        self.allPossibleMoves = []
        self.makeListAllPossibleMoves(gameState)
        return self.chooseMove(gameState)

    def makeListAllPossibleMoves(self, gameState):
        """Makes a list of all the possible moves for all the marbles"""

        #We take each marble one by one
        for marble in self.marblesPos:
            gameState.grid[marble[0]][marble[1]] = 0 #The current marble position is temporarily set to empty to avoid errors in case of jump move
            gameState.nbMovesInTurn = 0
            marblePossibleMoves = gameState.makeListOfAllowedMoves(*marble)
            movesToInvestigate = []
            if marblePossibleMoves != []:
                for cell in marblePossibleMoves:
                    if cell not in gameState.listCellsInTriangles:
                        #If the last cell isn't in one of the exterior triangles,
                        #it's a possible move
                        self.allPossibleMoves += [[marble, cell]]
                    if not gameState.moveIsSimple(marble, cell):
                        #If we have done a simple move, then no other move can be added
                        #So no need to investigate
                        movesToInvestigate += [[marble, cell]]
                gameState.nbMovesInTurn = 1
                while movesToInvestigate != []:
                    cellsInCurrentMove = movesToInvestigate[0]
                    marblePossibleMoves = gameState.makeListOfAllowedMoves(*cellsInCurrentMove[len(cellsInCurrentMove)-1])
                    if marblePossibleMoves is not None:
                        #If there are some possible moves
                        for cell in marblePossibleMoves:
                            #We look at all of them one by one
                            if cell not in cellsInCurrentMove:
                                #If the cell is already in the move earlier on, we don't look at it 
                                #because otherwise, infinite loop
                                movesToInvestigate += [movesToInvestigate[0] + [cell]]
                                if cell not in gameState.listCellsInTriangles:
                                    #If the last cell isn't in one of the exterior triangles,
                                    #it's a possible move
                                    self.allPossibleMoves += [movesToInvestigate[0] + [cell]]

                    del movesToInvestigate[0] #The move has been investigated so we can delete it and keep going

            gameState.grid[marble[0]][marble[1]] = 2 #The original marble position is set back to normal

        gameState.nbMovesInTurn = 0

    def chooseMove(self, gameState):
        """Chooses which move is best"""

        #Initialize the points array with 0
        self.points = [0]*len(self.allPossibleMoves)

        #Call all the functions that give points
        if self.nbEmptySpacesLeft() == 1:
            self.addPointsLastMarble()
            self.addPointsWinningMove()
        else:
            self.addPointsNbLinesForward()
            self.addPointsxPos()
            self.addPointsInTriangle()

        #Sort the possible moves according to points
        for i in range(len(self.points) - 1, 0, -1):
            for j in range(i):
                if self.points[j] > self.points[j + 1]:
                    self.points[j + 1], self.points[j] = self.points[j], self.points[j + 1]
                    self.allPossibleMoves[j + 1], self.allPossibleMoves[j] = self.allPossibleMoves[j], self.allPossibleMoves[j + 1]

        if gameState.gameSetup.difficultyAI == "HARD":
            #If the game is in hard move, the AI will choose a move with the maximum number of points
            max_value = self.points[len(self.points) - 1]
            indexes_with_max_value = []
            i = len(self.points) - 1
            while self.points[i] == max_value:
                indexes_with_max_value += [i]
                i -= 1
            index_chosen = random.choice(indexes_with_max_value)
            move_chosen = self.allPossibleMoves[index_chosen]
        
        if gameState.gameSetup.difficultyAI == "NORMAL":
            #If the game is in normal mode, the AI will randomly choose a move in the top 10% that isn't longer than 5,
            #and that has positive points
            indexes_to_choose_from = []
            beginning_i = int(len(self.points)*0.9)
            if self.nbEmptySpacesLeft() <= 3:
                #If there are 3 or less empty spaces left in the winning triangle,
                #the best move is automatically chosen to avoid infinite movement of the last marbles
                indexes_to_choose_from = [len(self.allPossibleMoves) - 1]
            else:
                for i in range (beginning_i, len(self.points)):
                    if len(self.allPossibleMoves[i]) <= 5 and self.points[i] > 0:
                        indexes_to_choose_from += [i]

            if indexes_to_choose_from == []:
                #If the indexes to choose from is still empty,
                #We take the best move
                indexes_to_choose_from += [len(self.allPossibleMoves) - 1]

            index_chosen = random.choice(indexes_to_choose_from)
            move_chosen = self.allPossibleMoves[index_chosen]

        if gameState.gameSetup.difficultyAI == "EASY":
            #If the game is in easy mode, the AI will randomly choose a move in the top 20%, that is not a very long move (not longer than 3)
            indexes_to_choose_from = []
            beginning_i = int(len(self.points)*0.8)
            if self.nbEmptySpacesLeft() <= 3:
                #If there are 3 or less empty spaces left in the winning triangle,
                #the best move is automatically chosen to avoid infinite movement of the last marbles
                indexes_to_choose_from = [len(self.allPossibleMoves) - 1]
            else:
                for i in range (beginning_i, len(self.points)):
                    #An easy AI won't make moves that are too long
                    if len(self.allPossibleMoves[i]) <= 3 and self.points[i] > 0:
                        indexes_to_choose_from += [i]

            if indexes_to_choose_from == []:
                #If the indexes to choose from is still empty,
                #We take the best move
                indexes_to_choose_from += [len(self.allPossibleMoves) - 1]

            index_chosen = random.choice(indexes_to_choose_from)
            move_chosen = self.allPossibleMoves[index_chosen]

        #We update the marble positions
        self.marblesPos[self.marblesPos.index(move_chosen[0])] = move_chosen[len(move_chosen)-1]
        return move_chosen

    def nbEmptySpacesLeft(self):
        """This function determines the number of empty spaces that are left
        in the AI winning triangle and returns that number"""
        AI_win_cells = [(12, 16), (11, 15), (13, 15), (10, 14), (12, 14), (14, 14), (9, 13), (11, 13), (13, 13), (15, 13)]
        nb_empty_spaces_left = 10
        for marble in self.marblesPos:
            if marble in AI_win_cells:
                nb_empty_spaces_left -= 1
        return nb_empty_spaces_left
    
    def posLastEmptyCell(self):
        """This function returns the position of the last empty space in the 
        AI winning triangle"""
        AI_win_cells = [(12, 16), (11, 15), (13, 15), (10, 14), (12, 14), (14, 14), (9, 13), (11, 13), (13, 13), (15, 13)]
        for cell in AI_win_cells:
            if cell not in self.marblesPos:
                return cell

    def posLastMarble(self):
        """This function returns the position of the last marble that isn't in the 
        AI winning triangle"""
        AI_win_cells = [(12, 16), (11, 15), (13, 15), (10, 14), (12, 14), (14, 14), (9, 13), (11, 13), (13, 13), (15, 13)]
        for marble in self.marblesPos:
            if marble not in AI_win_cells:
                return marble

    """These next functions all add or remove points to the possible moves"""

    def addPointsNbLinesForward(self):
        """This function adds 10 points per lines moved towards winning triangle (removes 10 if in wrong direction)
        There is also a multiplier that adds more points if the marble chosen is higher on the board
        (this makes it less likely to have cells that are left alone on top)"""
        for i in range (len(self.allPossibleMoves)):
            fromCell = self.allPossibleMoves[i][0]
            toCell = self.allPossibleMoves[i][len(self.allPossibleMoves[i])-1]
            multiplier = 2.7 - fromCell[1]*0.1
            self.points[i] = self.points[i] + (toCell[1] - fromCell[1])*(10+multiplier)

    def addPointsxPos(self):
        """This function adds 5 points if the end position is in the three most centered x positions
        It also adds points everytime you get closer to the center"""
        for i in range (len(self.allPossibleMoves)):
            end_cell = self.allPossibleMoves[i][len(self.allPossibleMoves[i])-1]
            if end_cell[0] in (11,12,13):
                self.points[i] = self.points[i] + 5
            beginning_cell = self.allPossibleMoves[i][0]
            dist_to_center_beginning = abs(12 - beginning_cell[0])
            dist_to_center_end = abs(12 - end_cell[0])
            if dist_to_center_beginning > dist_to_center_end:
                self.points[i] = self.points[i] + (dist_to_center_beginning - dist_to_center_end)*2
    
    def addPointsInTriangle(self):
        """This function adds 50 points if the move makes the marble go into the winning triangle (and it wasn't in it already)"""
        AI_win_cells = [(12, 16), (11, 15), (13, 15), (10, 14), (12, 14), (14, 14), (9, 13), (11, 13), (13, 13), (15, 13)]
        for i in range (len(self.allPossibleMoves)):
            fromCell = self.allPossibleMoves[i][0]
            toCell = self.allPossibleMoves[i][len(self.allPossibleMoves[i])-1]
            if fromCell not in AI_win_cells and toCell in AI_win_cells :
                self.points[i] = self.points[i] + 50
    
    def addPointsWinningMove(self):
        """This function adds 1000 points if the move makes the AI win"""
        AI_win_cells = [(12, 16), (11, 15), (13, 15), (10, 14), (12, 14), (14, 14), (9, 13), (11, 13), (13, 13), (15, 13)]
        cells_remaining = []
        for i in range (10):
            if self.marblesPos[i] not in AI_win_cells:
                cells_remaining += [self.marblesPos[i]]

        if len(cells_remaining) == 1:
            for i in range (len(self.allPossibleMoves)):
                cell = self.allPossibleMoves[i][len(self.allPossibleMoves[i])-1]
                if cell == cells_remaining[0]:
                    self.points[i] = self.points[i] + 1000

    def addPointsLastMarble(self):
        """This function is called when only one marble is left to place
        It adds points when the marble gets closer to the empty cell that is left
        (10 points everytime the x gets closer and 20 points everytime the y gets closer)"""
        #We first find what the positions of the last empty cell and the last marble are
        pos_last_empty_cell = self.posLastEmptyCell()
        empty_cell_x = pos_last_empty_cell[0]
        empty_cell_y = pos_last_empty_cell[1]
        pos_last_marble = self.posLastMarble()
        marble_x = pos_last_marble[0]
        marble_y = pos_last_marble[1]

        #We then calculate the position difference between the marble and the last empty cell
        diff_x = abs(marble_x - empty_cell_x)
        diff_y = abs(marble_y - empty_cell_y)

        #We look at every move
        for i in range (len(self.allPossibleMoves)):
            beginning_cell = self.allPossibleMoves[i][0]
            end_cell = self.allPossibleMoves[i][len(self.allPossibleMoves[i])-1]
            #We only look at the moves that are made with the last marble:
            if beginning_cell == pos_last_marble:
                end_cell_x = end_cell[0]
                end_cell_y = end_cell[1]
                new_diff_x = abs(end_cell_x - empty_cell_x)
                new_diff_y = abs(end_cell_y - empty_cell_y)
                #We now look if the new difference between the positions is smaller and add the points
                self.points[i] += (diff_x - new_diff_x)*10
                self.points[i] += (diff_y - new_diff_y)*20
