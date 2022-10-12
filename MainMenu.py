#!/usr/bin/env python
import os
import wx
from GraphicModeFunctions import *
from ManageSaves import *
import AboutandHowtoplay as ah
import Setup as s
import Game as g
#------------------------------------------------------------------------
class MainMenu(wx.Frame):

    def __init__(self, parent):
        """Class initializer"""
        wx.Frame.__init__(self, parent, title = 'Chinese Checkers - Main Menu', size = (1000, 700))
        self.drawScreen()
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

    def drawScreen(self):
        """Displays the screen"""
        self.SetBackgroundColour(backgroundColor)
        self.Center()
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.onToggle)
        #Display title
        displayText(self, 'Chinese checkers', 100, 100, 60)

        #Display buttons
        displayButton(self, 'About', x = 590, y = 500, width = 160, height = 50, size = 18, action = self.onAbout)
        displayButton(self, 'How To Play', 250, 500, 160, 50, 18, self.onHowToPlay)
        displayButton(self, 'Exit', 460, 580, 80, 30, 15, self.onExit)
        self.playButton = wx.ToggleButton(self, label = 'PLAY', pos = (375, 330), style = wx.BORDER_NONE)
        setupButton(btn = self.playButton, width = 250, height = 80, size = 35)

    def onPaint(self, event):
        """Reaction to EVT_PAINT
        Displays the decoration circles"""
        dc = wx.GCDC(wx.PaintDC(self))

        drawCircles(x = 250, y = 250, size = 25, spacing = 100, dc = dc)

    def onToggle(self, event):
        """Reaction the the EVT_TOGGLE event
        This function reacts when one of the toggle buttons is clicked.
        It gives the play button the right color
        """
        if self.playButton.GetValue():
            self.playButton.SetBackgroundColour(pressedButtonColor)
            displayButton(self, 'NEW GAME', 380, 430, 100, 40, 12, self.onNewGame)
            self.loadGameButton = wx.Button(self, label = 'LOAD GAME', pos = (520, 430),style = wx.BORDER_NONE)
            setupButton(btn = self.loadGameButton, width = 100, height = 40, size = 12)
            self.Bind(wx.EVT_BUTTON, self.onLoadGame, self.loadGameButton)
            self.loadGameButton.Disable()
            if os.path.exists("saveFile.txt"):
                self.loadGameButton.Enable()
            self.Refresh()

    """Functions that tell what needs to be done when a button is clicked:"""
    def onAbout(self, event):
        """Opens 'About' frame"""
        about = ah.About(self)
        about.SetMaxSize(wx.Size(1000,700))
        about.SetMinSize(wx.Size(1000,700))
        self.Show(False)

    def onNewGame(self, event):
        """Opens 'Setup' frame"""
        setup = s.Setup(self)
        setup.SetMaxSize(wx.Size(1000,700))
        setup.SetMinSize(wx.Size(1000,700))
        self.Show(False)

    def onLoadGame(self, event):
        """Opens 'Game' frame using the savefile"""
        game = g.Game(self, *extractSaveFile())
        game.SetMaxSize(wx.Size(1000,700))
        game.SetMinSize(wx.Size(1000,700))
        self.Show(False)

    def onHowToPlay(self, event):
        """Opens'HowToPlay' frame"""
        howToPlay = ah.HowToPlay(self)
        howToPlay.SetMaxSize(wx.Size(1000,700))
        howToPlay.SetMinSize(wx.Size(1000,700))
        self.Show(False)

    def onExit(self, event):
        """Closes the frame"""
        self.Destroy()
