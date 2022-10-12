#!/usr/bin/env python
import wx
from GraphicModeFunctions import *
import ManageSaves as ms
import Game as g

class GameOver(wx.Frame):

    def __init__(self, previous, gameSetup, gameState):
        """Class initializer"""
        super().__init__(None, title = 'Chinese Checkers - Game Over', size = (1000, 700))
        self.previous = previous
        self.gameSetup = gameSetup
        self.gameState = gameState
        self.drawScreen()
        self.Show()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

    def drawScreen(self):
        """Displays the screen"""
        self.Center()
        self.SetBackgroundColour(backgroundColor)
        self.Bind(wx.EVT_PAINT, self.onPaint)


        #Display text that needs to be centered
        gameOverText = wx.StaticText(self, label = 'GAME OVER', pos = (250, 30), style = wx.ALIGN_CENTER)
        setupTextInCenter(gameOverText, 40, 500)
        gameOverText.SetForegroundColour(whiteColor)
        gameOverText.SetBackgroundColour(backgroundColor)

        if self.gameState.winner is None:
            displayWinnerText = wx.StaticText(self, label = '): Nobody won :(', pos = (250, 120), style = wx.ALIGN_CENTER)
            setupTextInCenter(displayWinnerText, 30, 500)
            displayWinnerText.SetForegroundColour(whiteColor)
            displayWinnerText.SetBackgroundColour(backgroundColor)
        else:
            displayWinnerText = wx.StaticText(self, label = '!!!' + self.gameSetup.playerNames[self.gameState.winner - 1] + ' wins!!!', pos = (0, 120), style = wx.ALIGN_CENTER)
            setupTextInCenter(displayWinnerText, 30, 1000)
            displayWinnerText.SetForegroundColour(self.gameSetup.playerColors[self.gameState.winner - 1])
            displayWinnerText.SetBackgroundColour(backgroundColor)


        #Display score
        scoreText = wx.StaticText(self, label = "SCORE", pos = (0, 190), style = wx.ALIGN_CENTER)
        setupTextInCenter(scoreText, 25, 1000)
        scoreText.SetForegroundColour(whiteColor)
        scoreText.SetBackgroundColour(backgroundColor)
        player1score = wx.StaticText(self, label = str(self.gameState.score[0]), pos = (380, 230), style = wx.ALIGN_CENTER)
        setupTextInCenter(player1score, 40, 115)
        player1score.SetForegroundColour(self.gameSetup.playerColors[0])
        player1score.SetBackgroundColour(backgroundColor)
        player2score = wx.StaticText(self, label = str(self.gameState.score[1]), pos = (505, 230), style = wx.ALIGN_CENTER)
        setupTextInCenter(player2score, 40, 115)
        player2score.SetForegroundColour(self.gameSetup.playerColors[1])
        player2score.SetBackgroundColour(backgroundColor)
        displayText(self, ":", 485, 225, 40)

        #Display text
        statsText = wx.StaticText(self, label = 'STATS', pos = (430, 320), style = wx.ALIGN_CENTER)
        setupTextInCenter(statsText, 20, 140)
        statsText.SetForegroundColour(whiteColor)
        statsText.SetBackgroundColour(backgroundColor)

        displayplayer1name = wx.StaticText(self, label = self.gameSetup.playerNames[0], pos = (130, 330), style = wx.ALIGN_CENTER)
        setupTextInCenter(displayplayer1name, 18, 290)
        displayplayer1name.SetForegroundColour(whiteColor)
        displayplayer1name.SetBackgroundColour(rectangleColor)

        displayplayer2name = wx.StaticText(self, label = self.gameSetup.playerNames[1], pos = (580, 330), style = wx.ALIGN_CENTER)
        setupTextInCenter(displayplayer2name, 18, 290)
        displayplayer2name.SetForegroundColour(whiteColor)
        displayplayer2name.SetBackgroundColour(rectangleColor)

        displayText(self, "total number of turns: " + str(self.gameState.totalNbTurns[0]), 135, 410, 12)
        displayText(self, "number of simple moves: " + str(self.gameState.nbSimpleMoves[0]), 135, 440, 12)
        displayText(self, "number of jumps: " + str(self.gameState.totalNbJumps[0]), 135, 470, 12)
        displayText(self, "total number of turns: " + str(self.gameState.totalNbTurns[1]), 585, 410, 12)
        displayText(self, "number of simple moves: " + str(self.gameState.nbSimpleMoves[1]), 585, 440, 12)
        displayText(self, "number of jumps: " + str(self.gameState.totalNbJumps[1]), 585, 470, 12)

        #Display buttons
        displayButton(self, 'Play Again', 630, 550, 150, 60, 18, self.onPlayAgain)
        displayButton(self, 'Save && Quit', 220, 550, 150, 60, 18, self.onSave)
        displayButton(self, 'Exit', 460, 600, 80, 30, 15, self.onExit)

    def onPaint(self, event):
        """Reaction to the EVT_PAINT event
        Redraws the rectangles
        """
        dc = wx.GCDC(wx.PaintDC(self))
        drawRectangle(125, 310, 300, 200, dc)
        drawRectangle(575, 310, 300, 200, dc)
        drawOneCircle(275, 375, 13, None, self.gameSetup.playerColors[0], dc)
        drawOneCircle(725, 375, 13, None, self.gameSetup.playerColors[1], dc)


    """Functions that tell what needs to be done when a button is clicked:"""

    def onPlayAgain(self, event):
        """Opens a new Game window but keeps the score"""
        self.gameState.initializeGrid()
        self.gameState.resetVariables()
        if self.gameSetup.gameAgainstAI:
            self.gameState.currentPlayer = 1
        game = g.Game(self.previous, self.gameSetup, self.gameState)
        game.SetMaxSize(wx.Size(1000,700))
        game.SetMinSize(wx.Size(1000,700))
        self.Destroy()

    def onSave(self, event):
        """Saves the setup and state of the game and closes the window"""
        self.gameSetup.playerColors[0] = allMarbleColors.index(self.gameSetup.playerColors[0])
        self.gameSetup.playerColors[1] = allMarbleColors.index(self.gameSetup.playerColors[1])
        if (self.gameState.winner != None):
            self.gameState.initializeGrid()
            self.gameState.resetVariables()
        ms.createSaveFile(self.gameSetup, self.gameState)
        if self.previous:
            self.previous.loadGameButton.Enable()
            self.previous.Show()
        self.Destroy()

    def onClose(self, event):
        """Destroys the current frame and goes to main menu when closed by user"""
        if self.previous:
            self.previous.Show()
        self.Destroy()

    def onExit(self, event):
        """Destroys all the frames"""
        if self.previous:
            self.previous.Destroy()
        self.Destroy()
