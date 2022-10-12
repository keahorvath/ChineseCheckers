#!/usr/bin/env python
import random
import wx
from GraphicModeFunctions import *
import GameState as gs
import Game as g

class Setup(wx.Frame):

    def __init__(self, previous):
        super().__init__(None, title = 'Chinese Checkers - Game Setup', size = (1000, 700))
        self.previous = previous
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

        #Setup all bind functions
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadio)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.onToggle)

        #Display Back button
        displayButton(self, 'Back', x = 20, y = 20, width = 100, height = 40, size = 16, action = self.onClose)

        #Display Start button
        self.startButton = wx.Button(self, label = 'START', pos = (400, 580),style = wx.BORDER_NONE)
        setupButton(btn = self.startButton, width = 200, height = 60, size = 25)
        self.Bind(wx.EVT_BUTTON, self.onStart, self.startButton)

        #Display text
        displayText(self, 'SETUP', x = 420, y = 20, size = 40)
        displayText(self, 'OR', 475, 260, 27)
        displayText(self, "Enter player 1 name:", 175, 160, 12)
        displayText(self, "Choose your color:", 183, 230, 12)
        displayText(self, "Enter player 2 name:", 175, 310, 12)
        displayText(self, "Choose your color:", 183, 380, 12)
        displayText(self, "Enter player name:", 635, 160, 12)
        displayText(self, "Choose your color:", 634, 230, 12)
        displayText(self, "Choose game difficulty:", 610, 350, 12)

        #Display toggle buttons
        self.gameMode1Button = wx.ToggleButton(self, label = '1 VS 1', pos = (215, 100), style = wx.BORDER_NONE)
        setupButton(btn = self.gameMode1Button, width = 120, height = 40, size = 16)
        self.gameMode1Button.SetValue(True)
        self.gameMode1Button.SetBackgroundColour(pressedButtonColor)
        self.gameMode2Button = wx.ToggleButton(self, label = '1 VS AI', pos = (665, 100), style = wx.BORDER_NONE)
        setupButton(self.gameMode2Button, 120, 40, 16)
        self.easyModeButton = wx.ToggleButton(self, label = 'EASY', pos = (595, 390), style = wx.BORDER_NONE)
        setupButton(self.easyModeButton, 80, 40, 12)
        self.normalModeButton = wx.ToggleButton(self, label = 'NORMAL', pos = (685, 390), style = wx.BORDER_NONE)
        setupButton(self.normalModeButton, 80, 40, 12)
        self.hardModeButton = wx.ToggleButton(self, label = 'HARD', pos = (775, 390), style = wx.BORDER_NONE)
        setupButton(self.hardModeButton, 80, 40, 12)

        #Display text controls
        self.enterPlayerName1 = wx.TextCtrl(self, pos = (195, 185),style = wx.BORDER_NONE | wx.TE_CENTER)
        setupTextControl(self.enterPlayerName1)
        self.enterPlayerName2 = wx.TextCtrl(self, pos = (195, 335),style = wx.BORDER_NONE | wx.TE_CENTER)
        setupTextControl(self.enterPlayerName2)
        self.enterPlayerName = wx.TextCtrl(self, pos = (645, 185),style = wx.BORDER_NONE | wx.TE_CENTER)
        setupTextControl(self.enterPlayerName)

        #Draw lines
        drawLine(self, x = 195, y = 209)
        drawLine(self, 195, 359)
        drawLine(self, 645, 209)

        #Display radio buttons
        self.player1RadioButton1 = wx.RadioButton(self, style = wx.RB_GROUP)
        self.player1RadioButtons = [self.player1RadioButton1] + [wx.RadioButton(self) for i in range(5)]
        displayRadioButtons(self.player1RadioButtons, 169, 288)
        self.player1RadioButtons[1].Disable()

        self.player2RadioButton2 = wx.RadioButton(self, style = wx.RB_GROUP)
        self.player2RadioButtons = [wx.RadioButton(self), self.player2RadioButton2] + [wx.RadioButton(self) for i in range(4)]
        displayRadioButtons(self.player2RadioButtons, 169, 438)
        self.player2RadioButtons[0].Disable()

        self.playerRadioButton1 = wx.RadioButton(self, style = wx.RB_GROUP)
        self.playerRadioButtons = [self.playerRadioButton1] + [wx.RadioButton(self) for i in range(5)]
        displayRadioButtons(self.playerRadioButtons, 619, 288)

        #Display game mode text and toggle buttons
        chooseGameModeText = wx.StaticText(self, label = 'CHOOSE A GAME MODE', pos = (0, 480), style = wx.ALIGN_CENTER)
        setupTextInCenter(chooseGameModeText, 14, 1000)
        chooseGameModeText.SetBackgroundColour(backgroundColor)
        self.classicModeButton = wx.ToggleButton(self, label = 'CLASSIC', pos = (380, 510), style = wx.BORDER_NONE)
        setupButton(self.classicModeButton, 110, 40, 12)
        self.fastModeButton = wx.ToggleButton(self, label = 'FAST-PACED', pos = (510, 510), style = wx.BORDER_NONE)
        setupButton(self.fastModeButton, 110, 40, 12)
        self.fastModeButton.SetValue(True)
        self.fastModeButton.SetBackgroundColour(pressedButtonColor)

    def onPaint(self, event):
        """Reaction to the EVT_PAINT event
        Redraws the rectangles and circles
        """
        dc = wx.GCDC(wx.PaintDC(self))
        drawRectangle(x = 125, y = 85, width = 300, height = 380, dc = dc)
        drawRectangle(575, 85, 300, 380, dc)
        drawCircles(x = 175, y = 270, size = 12, spacing = 40, dc = dc)
        drawCircles(175, 420, 12, 40, dc)
        drawCircles(625, 270, 12, 40, dc)

    def onToggle(self, event):
        """Reaction the the EVT_TOGGLE event
        This function reacts when one of the toggle buttons is clicked.
        It makes sure that two buttons that are incompatible aren't pressed at the same time
        """
        eventObject = event.GetEventObject()
        self.gameLevelButtons = [self.easyModeButton, self.normalModeButton, self.hardModeButton]
        self.toggleButtons = [self.gameMode1Button, self.gameMode2Button, self.easyModeButton, self.normalModeButton, self.hardModeButton, self.classicModeButton, self.fastModeButton]

        #If you press 1 game mode button (1VS1 or 1VSAI) and the other one is already pressed, the other one gets unpressed
        if eventObject == self.gameMode1Button and self.gameMode2Button.GetValue():
            self.gameMode2Button.SetValue(False)
            self.easyModeButton.SetValue(False)
            self.normalModeButton.SetValue(False)
            self.hardModeButton.SetValue(False)
        if eventObject == self.gameMode2Button and self.gameMode1Button.GetValue():
            self.gameMode1Button.SetValue(False)
            self.easyModeButton.SetValue(True)

        #If you press 1 game mode button and the other one is already pressed, the other one gets unpressed
        if eventObject == self.classicModeButton and self.fastModeButton.GetValue():
            self.fastModeButton.SetValue(False)

        if eventObject == self.fastModeButton and self.classicModeButton.GetValue():
            self.classicModeButton.SetValue(False)

        #If you try to click on a level button while the 1 vs AI button isn't pressed, nothing happens
        if (eventObject in self.gameLevelButtons) and not self.gameMode2Button.GetValue():
            eventObject.SetValue(False)

        #Only one level button can be pressed at a time
        if eventObject == self.easyModeButton:
            self.normalModeButton.SetValue(False)
            self.hardModeButton.SetValue(False)
        if eventObject == self.normalModeButton:
            self.easyModeButton.SetValue(False)
            self.hardModeButton.SetValue(False)
        if eventObject == self.hardModeButton:
            self.normalModeButton.SetValue(False)
            self.easyModeButton.SetValue(False)

        #If you unclick the 1 vs AI button, any level button that is pressed will be unpressed
        if eventObject == self.gameMode2Button and not eventObject.GetValue():
            for i in self.gameLevelButtons:
                i.SetValue(False)

        #If all buttons are pressed on one side, you can press start
        if (self.gameMode1Button.GetValue() or (self.gameMode2Button.GetValue() and (self.easyModeButton.GetValue() or self.normalModeButton.GetValue() or self.hardModeButton.GetValue()))) and (self.classicModeButton.GetValue() or self.fastModeButton.GetValue()):
            self.startButton.Enable()
        else:
            self.startButton.Disable()

        #Gives the right color to each button
        for i in self.toggleButtons:
            if i.GetValue():
                i.SetBackgroundColour(pressedButtonColor)
            else:
                i.SetBackgroundColour(buttonColor)

    def onRadio(self, event):
        """Reaction the the EVT_RADIO event
        This function reacts when one of the radio buttons is clicked.
        It makes sure that two buttons that are incompatible aren't pressed at the same time
        """
        #Makes it so that the two players can't have the same color
        eventObject = event.GetEventObject()
        if eventObject in self.player1RadioButtons:
            for i in self.player2RadioButtons:
                i.Enable()
            self.player2RadioButtons[self.player1RadioButtons.index(eventObject)].Disable()

        if eventObject in self.player2RadioButtons:
            for i in self.player1RadioButtons:
                i.Enable()
            self.player1RadioButtons[self.player2RadioButtons.index(eventObject)].Disable()

    def onClose(self, event):
        """Destroys the frame when the game is closed by user"""
        if self.previous:
            self.previous.Show()
        self.Destroy()

    def onStart(self, event):
        """Function that is called when the user presses the "start" button
        It gathers the information given by the user in the setup and opens the game frame
        """
        gameSetup = gs.GameSetup()
        if self.gameMode1Button.GetValue():
            gameSetup.gameAgainstAI = False
            for i in self.player1RadioButtons:
                if i.GetValue():
                    gameSetup.playerColors += [allMarbleColors[self.player1RadioButtons.index(i)]]
            for i in self.player2RadioButtons:
                if i.GetValue():
                    gameSetup.playerColors += [allMarbleColors[self.player2RadioButtons.index(i)]]

            gameSetup.playerNames[0] = self.enterPlayerName1.GetLineText(0)
            gameSetup.playerNames[1] = self.enterPlayerName2.GetLineText(0)

        if self.gameMode2Button.GetValue():
            gameSetup.gameAgainstAI = True
            for btn in self.playerRadioButtons:
                if btn.GetValue():
                    gameSetup.playerColors += [allMarbleColors[self.playerRadioButtons.index(btn)]]
                    indexes = [0,1,2,3,4,5]
                    indexes.remove(self.playerRadioButtons.index(btn))
                    gameSetup.playerColors += [allMarbleColors[random.choice(indexes)]]
            gameSetup.playerNames[0] = self.enterPlayerName.GetLineText(0)
            if self.easyModeButton.GetValue():
                gameSetup.playerNames[1] = "EASY AI"
                gameSetup.difficultyAI = gameSetup.easy
            if self.normalModeButton.GetValue():
                gameSetup.playerNames[1] = "NORMAL AI"
                gameSetup.difficultyAI = gameSetup.normal
            if self.hardModeButton.GetValue():
                gameSetup.playerNames[1] = "HARD AI"
                gameSetup.difficultyAI = gameSetup.hard

        if self.classicModeButton.GetValue():
            gameSetup.gameMode = gameSetup.classicMode
        else:
            gameSetup.gameMode = gameSetup.fastPacedMode

        game = g.Game(self.previous, gameSetup, None)
        game.SetMaxSize(wx.Size(1000,700))
        game.SetMinSize(wx.Size(1000,700))
        self.Destroy()
