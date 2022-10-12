#!/usr/bin/env python
import wx
from GraphicModeFunctions import *

class About(wx.Frame):

    def __init__(self, previous):
        """Class initializer"""
        super().__init__(None, title = 'Chinese Checkers - About', size = (1000, 700))
        self.previous = previous
        self.drawScreen()
        self.Show()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

    def drawScreen(self):
        """Displays the screen"""
        self.SetBackgroundColour(backgroundColor)
        self.Center()
        displayButton(self, 'Back', x = 20, y = 20, width = 100, height = 40, size = 16, action = self.onClose)
        displayText(self, 'ABOUT', 420, 40, 40)
        displayText(self, 'This game was programmed by Kea Horvath for her "CMI Projet Programmation" class in fall 2020.', 40, 130, 13)
        displayText(self, 'If you notice any bugs in the game, please report them to the following email address:', 40, 160, 13)
        displayText(self, 'kea.horvath@etu.u-bordeaux.fr', 40, 190, 13)
        displayText(self, 'For further information about the program or how the game works,', 40, 340, 13)
        displayText(self, 'Please read the developer and user documentation that came with the game.', 40, 370, 13)
        displayText(self, 'Hope you enjoy my game!', 40, 520, 13)

        self.Bind(wx.EVT_PAINT, self.onPaint)

    def onPaint(self, event):
        """Displays the decoration circles"""
        dc = wx.GCDC(wx.PaintDC(self))

        drawOneCircle(x = 25, y = 140, size = 8, border = None, color = lightBlueColor, dc = dc)
        drawOneCircle(x = 25, y = 170, size = 8, border = None, color = pinkColor, dc = dc)
        drawOneCircle(x = 25, y = 200, size = 8, border = None, color = purpleColor, dc = dc)
        drawOneCircle(x = 25, y = 350, size = 8, border = None, color = greenColor, dc = dc)
        drawOneCircle(x = 25, y = 380, size = 8, border = None, color = whiteColor, dc = dc)
        drawOneCircle(x = 25, y = 530, size = 8, border = None, color = darkBlueColor, dc = dc)

    def onClose(self, event):
        """Destroys the frame when the game is closed by user"""
        if self.previous:
            self.previous.Show()
        self.Destroy()

#------------------------------------------------------------------------
class HowToPlay(wx.Frame):

    def __init__(self, previous):
        """Class initializer"""
        super().__init__(None, title = 'Chinese Checkers - How To Play', size = (1000, 700))
        self.previous = previous
        self.drawScreen()
        self.Show()
        self.Bind(wx.EVT_CLOSE, self.onClose)
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

    def drawScreen(self):
        """Displays the screen"""
        self.SetBackgroundColour(backgroundColor)
        self.Center()

        displayButton(self, 'Back', x = 20, y = 20, width = 100, height = 40, size = 16, action = self.onClose)

        displayText(self, 'HOW TO PLAY', 320, 40, 40)

        displayText(self, 'GOAL OF THE GAME:', 60, 110, 17)
        displayText(self, '- The aim of Chinese Checkers is to move all your marbles from your starting triangle base', 40, 140, 12.5)
        displayText(self, '  to the opposite triangle base, before your opponent does so.', 40, 160, 12.5)

        displayText(self, 'BEGINNING THE GAME:', 60, 200, 17)
        displayText(self, '- The first player to play is chosen at random by the computer.', 40, 230, 12.5)

        displayText(self, 'RULES:', 60, 270, 17)
        displayText(self, '- Rule n°1: You can move a marble to the space right next to it, if it is empty.', 40, 300, 12.5)
        displayText(self, '- Rule n°2 (CLASSIC MODE): You can jump over an adjacent marble, if the space directly', 40, 330, 12.5)
        displayText(self, '  behind it is empty.', 40, 350, 12.5)
        displayText(self, '- Rule n°2 (FAST-PACED MODE): You can jump over another marble in a straight line,', 40, 380, 12.5)
        displayText(self, '  even skipping empty spaces.', 40, 400, 12.5)
        displayText(self, '- Rule n°3: After jumping over a marble, you can use that same marble to jump again', 40, 430, 12.5)
        displayText(self, '  in the same turn.', 40, 450, 12.5)
        displayText(self, '- Rule n°4: You cannot end a move in a base that is not yours or your opponent’s base,', 40, 480, 12.5)
        displayText(self, '  but you can jump into and out of those bases during a turn.', 40, 500, 12.5)

        displayText(self, 'GAMEPLAY:', 60, 540, 17)
        displayText(self, '- Click on a marble to select it.', 40, 570, 12.5)
        displayText(self, '- Make as many moves as you want and then click on the selected marble to end your turn.', 40, 600, 12.5)

        self.Bind(wx.EVT_PAINT, self.onPaint)

    def onPaint(self, event):
        """Displays the decoration circles"""
        dc = wx.GCDC(wx.PaintDC(self))

        drawOneCircle(x = 30, y = 120, size = 12, border = None, color = lightBlueColor, dc = dc)
        drawOneCircle(x = 30, y = 210, size = 12, border = None, color = pinkColor, dc = dc)
        drawOneCircle(x = 30, y = 280, size = 12, border = None, color = greenColor, dc = dc)
        drawOneCircle(x = 30, y = 550, size = 12, border = None, color = purpleColor, dc = dc)


    def onClose(self, event):
        """Destroys the frame when the game is closed by user"""
        if self.previous:
            self.previous.Show()
        self.Destroy()
