#!/usr/bin/env python
import math
import time
import wx
from GraphicModeFunctions import *
import GameState as gs
import ManageSaves as ms
import AboutandHowtoplay as ah
import GameOver as go
from AI import AI


class Game(wx.Frame):

    def __init__(self, previous, gameSetup, gameState):
        """Class initializer"""
        super().__init__(None, title = 'Chinese Checkers - Game', size = (1000, 700))
        self.previous = previous
        self.gameSetup = gameSetup

        if gameState is None:
            self.gameState = gs.GameState(self.gameSetup)
        else:
            self.gameState = gameState
            self.gameState.gameSetup = self.gameSetup
        self.AI = AI(self.gameState)
        self.AImoves = []
        self.nbMovesAI = 0
        self.drawScreen()
        self.Show()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onClick)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.onToggle)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.timer = wx.Timer(self)

    def drawScreen(self):
        """Displays the screen (buttons and text)"""
        self.SetBackgroundColour(backgroundColor)
        self.Center()
        
        self.helpButton = wx.Button(self, label = '?', pos = (600, 570), style = wx.BORDER_NONE)
        setupButton(btn = self.helpButton, width = 40, height = 40, size = 29)
        self.Bind(wx.EVT_BUTTON, self.onHelp, self.helpButton)

        #Display Game Mode
        gameModeText = wx.StaticText(self, label = self.gameSetup.gameMode, pos = (705, 60), style = wx.ALIGN_CENTER)
        setupTextInCenter(gameModeText, 18, 240)

        drawLine(self, 750, 90)

        #Display player names
        if self.gameSetup.playerNames[0] == "":
            self.gameSetup.playerNames[0] = "Player 1"
        if self.gameSetup.playerNames[1] == "":
            self.gameSetup.playerNames[1] = "Player 2"
        self.player1text = wx.StaticText(self, label = self.gameSetup.playerNames[0], pos = (705, 100), style = wx.ALIGN_CENTER)
        setupTextInCenter(self.player1text, 13, 240)
        self.player2text = wx.StaticText(self, label = self.gameSetup.playerNames[1], pos = (705, 160), style = wx.ALIGN_CENTER)
        setupTextInCenter(self.player2text, 13, 240)

        #Display arrows that indicate whose turn it is
        self.arrow1 = wx.StaticText(self, label = "-->", pos = (710, 100))
        self.arrow1.SetFont(wx.Font(16,wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        self.arrow1.SetForegroundColour(goldColor)
        self.arrow1.SetBackgroundColour(rectangleColor)
        self.arrow2 = wx.StaticText(self, label = "-->", pos = (710, 160))
        self.arrow2.SetFont(wx.Font(16,wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        self.arrow2.SetForegroundColour(goldColor)
        self.arrow2.SetBackgroundColour(rectangleColor)
        self.showCurrentPlayer()

        drawLine(self, 750, 220)

        #Display score
        scoreText = wx.StaticText(self, label = "SCORE", pos = (705, 230), style = wx.ALIGN_CENTER)
        setupTextInCenter(scoreText, 22, 240)
        scoreText.SetBackgroundColour(rectangleColor)

        player1score = wx.StaticText(self, label = str(self.gameState.score[0]), pos = (705, 260), style = wx.ALIGN_CENTER)
        setupTextInCenter(player1score, 35, 115)
        player1score.SetForegroundColour(self.gameSetup.playerColors[0])
        player1score.SetBackgroundColour(rectangleColor)
        player2score = wx.StaticText(self, label = str(self.gameState.score[1]), pos = (830, 260), style = wx.ALIGN_CENTER)
        setupTextInCenter(player2score, 35, 115)
        player2score.SetForegroundColour(self.gameSetup.playerColors[1])
        player2score.SetBackgroundColour(rectangleColor)
        displayText(self, ":", 815, 260, 30)

        drawLine(self, 750, 315)

        #Display help on/off buttons
        displayText(self, "Display possible moves", 712, 330, 12)
        self.helpOnButton = wx.ToggleButton(self, label = 'ON', pos = (745,360), style = wx.BORDER_NONE)
        setupButton(self.helpOnButton, 60, 35, 15)
        self.helpOffButton = wx.ToggleButton(self, label = 'OFF', pos = (845,360), style = wx.BORDER_NONE)
        setupButton(self.helpOffButton, 60, 35, 15)
        self.helpOnButton.SetValue(True)
        self.helpOnButton.SetBackgroundColour(pressedButtonColor)

        drawLine(self, 750, 410)

        #Display Undo button
        self.undoButton = wx.Button(self, label = 'UNDO', pos = (780, 425),style = wx.BORDER_NONE)
        setupButton(btn = self.undoButton, width = 90, height = 40, size = 15)
        self.Bind(wx.EVT_BUTTON, self.onUndo, self.undoButton)
        self.undoButton.Disable()
        drawLine(self, 750, 480)

        #Display restart and main menu button
        self.restartButton = wx.Button(self, label = 'Restart', pos = (725, 540),style = wx.BORDER_NONE)
        setupButton(btn = self.restartButton, width = 90, height = 40, size = 12)
        self.Bind(wx.EVT_BUTTON, self.onRestart, self.restartButton)
        self.saveButton = wx.Button(self, label = 'Save && Quit', pos = (765, 490),style = wx.BORDER_NONE)
        setupButton(btn = self.saveButton, width = 120, height = 40, size = 12)
        self.Bind(wx.EVT_BUTTON, self.onSave, self.saveButton)
        self.overButton = wx.Button(self, label = 'Game Over', pos = (835, 540),style = wx.BORDER_NONE)
        setupButton(btn = self.overButton, width = 90, height = 40, size = 12)
        self.Bind(wx.EVT_BUTTON, self.onGameOver, self.overButton)


    def drawBoard(self):
        """Draws the whole board, and draws the right circle in each position of the grid,
        according to the current state of the game"""
        dc = wx.GCDC(wx.PaintDC(self))

        #Draws the circles(player1 marble, player2 marble, holes)
        for i in range(25):
            for j in range(17):
                if self.gameState.getCell(i, j) == 0:
                    drawOneCircle(110 + 20*i, 49 + 35*j, 13, None, holeColor, dc)
                if self.gameState.getCell(i, j) == 1:
                    drawOneCircle(110 + 20*i, 49 + 35*j, 13, None, self.gameSetup.playerColors[0], dc)
                if self.gameState.getCell(i, j) == 2:
                    drawOneCircle(110 + 20*i, 49 + 35*j, 13, None, self.gameSetup.playerColors[1], dc)

        #Draws the selected marble in the right place and with the right color
        if self.gameState.selectedMarble is not None:
            drawOneCircle(110 + 20*self.gameState.selectedMarble[0], 49 + 35*self.gameState.selectedMarble[1], 13, holeColor, self.gameSetup.playerColors[self.gameState.currentPlayer - 1], dc)

        #Draws all the allowed moves for a given selected marble
        #(This part can be disabled by the user with a button)
        if self.helpOffButton.GetValue() or (self.gameSetup.gameAgainstAI and self.gameState.currentPlayer == 2):
            for cell in self.gameState.allowedMoves:
                (current_x, current_y) = cell
                drawOneCircle(110 + 20*current_x, 49 + 35*current_y, 13, None, holeColor, dc)

        elif self.helpOnButton.GetValue():
            for cell in self.gameState.allowedMoves:
                (current_x, current_y) = cell
                drawOneCircle(110 + 20*current_x, 49 + 35*current_y, 13, self.gameSetup.playerColors[self.gameState.currentPlayer - 1], holeColor, dc)


    def positionToCell(self, x, y):
        """Returns the cell of the circle in the grid if a circle is clicked
        if player clicked outside of a circle, returns None
        Described in detail in the developer documentation (3.2)
        """
        #j represents the row of the clicked spot
        #i represents the column of the clicked spot
        j = int((y - 36)/35)
        if j % 2 == 0:
            i = int((x - 97)/40)*2
        else:
            i = int((x - 117)/40)*2 + 1

        if i > 24 or j > 16:
            #If the player clicked outside of the grid (outside of the board), return None
            return None

        if self.gameState.getCell(i, j) is None:
            #If the player clicked in the board, but the cell that he clicked isn't a circle, return None
            return None

        #We now know that the player clicked in a valid cell in the grid, but we have to make sure that he clicked exactly inside of the circle and not around it
        #To do that, we calculate the x and y center of the clicked cell (which is the center of the circle)
        #and then the x and y distance that separates the clicked x and y from the center x and y
        #Then, calculates the real distance that separates the clicked area from the center
        #If the result is bigger than 13 (which is the radius of a circle) return None
        center_x_pos = 110 + 20*i
        center_y_pos = 49 + 35*j
        dist_center_x = center_x_pos - x
        dist_center_y = center_y_pos - y
        if math.pow(dist_center_x,2) + math.pow(dist_center_y,2) > math.pow(13,2):
            return None

        #The player clicked inside of a circle so return the i and j values
        return (i, j)

    def showCurrentPlayer(self):
        """Changes the color of the current player
        and puts an arrow in front"""
        if self.gameState.currentPlayer == 1:
            self.player1text.SetForegroundColour(goldColor)
            self.player2text.SetForegroundColour(whiteColor)
            self.arrow1.Show()
            self.arrow2.Hide()
        if self.gameState.currentPlayer == 2:
            self.player1text.SetForegroundColour(whiteColor)
            self.player2text.SetForegroundColour(goldColor)
            self.arrow2.Show()
            self.arrow1.Hide()
    
    def onTimer(self, event):
        """Reaction to the EVT_TIMER event
        Is called in case of game against AI
        Allows to see each AI move individually by making breaks
        """
        turn = None
        if self.nbMovesAI == 0:
            turn = self.gameState.play(*self.AImoves[0])
            self.Refresh()
            del self.AImoves[0]
            self.timer.Stop()
        elif self.nbMovesAI == 1:
            turn = self.gameState.play(*self.AImoves[0])
            self.Refresh()
            self.nbMovesAI -= 1
        elif self.nbMovesAI > 1:
            turn = self.gameState.play(*self.AImoves[0])
            self.Refresh()
            del self.AImoves[0]
            self.nbMovesAI -= 1

        if turn == "turn is over":
            self.showCurrentPlayer()
            self.undoButton.Enable()
            self.saveButton.Enable()
            self.restartButton.Enable()
            self.overButton.Enable()

            if self.gameState.isGameOver():
                self.gameState.winner = 3 - self.gameState.currentPlayer
                self.gameState.score[self.gameState.winner - 1] += 1
                self.onGameOver(event)

    def onPaint(self, event):
        """Reaction to the EVT_PAINT event
        Redraws the rectangle, the board circle, the player circles and calls the drawBoard function
        """
        dc = wx.GCDC(wx.PaintDC(self))
        drawRectangle(700, 50, 250, 550, dc)
        drawOneCircle(350, 330, 300, "white", boardColor, dc)
        self.drawBoard()
        #Display player colors
        drawOneCircle(826, 140, 13, None, self.gameSetup.playerColors[0], dc)
        drawOneCircle(826, 200, 13, None, self.gameSetup.playerColors[1], dc)

    def onClick(self, event):
        """Reaction to the EVT_LEFT_DOWN event
        This function checks if the click is valid and calls the play function (from gameState)
        It also shows to the users whose turn it is and displays the winner if the game is over
        """
        pos = event.GetLogicalPosition(wx.ClientDC(self))
        cell = self.positionToCell(pos.x, pos.y)
        if cell is not None:
            #If the player clicked on a circle, call play function
            turn = self.gameState.play(*cell)
            self.Refresh()
            if turn == "turn is over":
                #If after playing that move, the turn is over,
                #buttons are enabled
                self.showCurrentPlayer()
                self.undoButton.Enable()
                self.saveButton.Enable()
                self.restartButton.Enable()
                self.overButton.Enable()
                if self.gameState.isGameOver():
                    #If the game is over after the turn,
                    #call game over function
                    self.gameState.winner = 3 - self.gameState.currentPlayer
                    self.gameState.score[self.gameState.winner - 1] += 1
                    self.onGameOver(event)
                elif self.gameSetup.gameAgainstAI:
                    #If the game is against an AI,
                    #call moveAI function and start timer
                    self.undoButton.Disable()
                    self.saveButton.Disable()
                    self.restartButton.Disable()
                    self.overButton.Disable()
                    self.AImoves = self.AI.moveAI(self.gameState)
                    self.nbMovesAI = len(self.AImoves)
                    self.timer.Start(400)
            else:
                #If the turn isn't over, disable buttons
                self.undoButton.Disable()
                self.saveButton.Disable()
                self.restartButton.Disable()
                self.overButton.Disable()

    def onToggle(self, event):
        """Reaction the the EVT_TOGGLE event
        This function reacts when one of the toggle buttons is clicked.
        It makes sure that two incompatible buttons aren't pressed at the same time
        """
        helpButtons = [self.helpOnButton, self.helpOffButton]
        eventObject = event.GetEventObject()
        self.helpOnButton.SetValue(self.helpOnButton == eventObject)
        self.helpOffButton.SetValue(self.helpOffButton == eventObject)

        for btn in helpButtons:
            if btn.GetValue():
                btn.SetBackgroundColour(pressedButtonColor)
            else:
                btn.SetBackgroundColour(buttonColor)

    """Functions that tell what needs to be done when a button is clicked:"""

    def onUndo(self, event):
        """Undos the previous move"""
        if self.gameState.previousMove != [None, None]:
            cellToMove1 = self.gameState.previousMove[0]
            cellToMove2 = self.gameState.previousMove[1]
            if len(self.gameState.previousMove) == 2:
                self.gameState.currentPlayer = 3 - self.gameState.currentPlayer
                self.gameState.grid[cellToMove2[0]][cellToMove2[1]] = 0
                self.gameState.grid[cellToMove1[0]][cellToMove1[1]] = self.gameState.currentPlayer
                self.showCurrentPlayer()
                self.gameState.totalNbTurns[self.gameState.currentPlayer - 1] -= 1
            else:
                cellToMove3 = self.gameState.previousMove[2]
                cellToMove4 = self.gameState.previousMove[3]
                self.gameState.grid[cellToMove2[0]][cellToMove2[1]] = 0
                self.gameState.grid[cellToMove1[0]][cellToMove1[1]] = self.gameState.currentPlayer
                self.gameState.grid[cellToMove4[0]][cellToMove4[1]] = 0
                self.gameState.grid[cellToMove3[0]][cellToMove3[1]] = 3 - self.gameState.currentPlayer
                self.AI.marblesPos[self.AI.marblesPos.index(cellToMove4)] = (cellToMove3[0], cellToMove3[1])
                self.gameState.totalNbTurns[0] -= 1
                self.gameState.totalNbTurns[1] -= 1
               
            self.gameState.nbSimpleMoves = self.gameState.previousNbSimpleMoves
            self.gameState.totalNbJumps = self.gameState.previousTotalNbJumps
            self.undoButton.Disable()
            self.Refresh()

    def onHelp(self, event):
        """Opens the HowToPlay window""" 
        howToPlay = ah.HowToPlay(self)
        howToPlay.SetMaxSize(wx.Size(1000,700))
        howToPlay.SetMinSize(wx.Size(1000,700))
        self.Show(False)

    def onRestart(self, event):
        """Restarts the current game but keeps the score"""
        self.gameState.initializeGrid()
        self.gameState.resetVariables()
        game = Game(self.previous, self.gameSetup, self.gameState)
        game.SetMaxSize(wx.Size(1000,700))
        game.SetMinSize(wx.Size(1000,700))
        self.Destroy()

    def onSave(self, event):
        """Saves the current state of the game"""
        self.gameSetup.playerColors[0] = allMarbleColors.index(self.gameSetup.playerColors[0])
        self.gameSetup.playerColors[1] = allMarbleColors.index(self.gameSetup.playerColors[1])
        ms.createSaveFile(self.gameSetup, self.gameState)
        if self.previous:
            self.previous.loadGameButton.Enable()
            self.previous.Show()
        self.Destroy()

    def onGameOver(self, event):
        gameover = go.GameOver(self.previous, self.gameSetup, self.gameState)
        gameover.SetMaxSize(wx.Size(1000,700))
        gameover.SetMinSize(wx.Size(1000,700))
        self.Destroy()

    def onClose(self, event):
        """Destroys the frame when the game is closed by user"""
        if self.previous:
            self.previous.Show()
        self.Destroy()
