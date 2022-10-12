#!/usr/bin/env python
import wx

"""These functions complete the GraphicMode.py file"""

#General Colors
buttonColor = wx.Colour(60,60,160)
backgroundColor = wx.Colour(50,50,100)
whiteColor = wx.Colour(255,255,255)
rectangleColor = wx.Colour(65,65,115)
boardColor = wx.Colour(80, 80, 150)
holeColor = wx.Colour(40, 40, 110)
goldColor = wx.Colour(255, 247, 80)
pressedButtonColor = wx.Colour(150,200,250)

#Marble Colors
lightBlueColor = wx.Colour(133,215,245)
darkBlueColor = wx.Colour(50,50,255)
purpleColor = wx.Colour(165,37,240)
pinkColor = wx.Colour(245,88,240)
greenColor = wx.Colour(0,250,146)
whiteColor = wx.Colour(255,255,255)
allMarbleColors = [lightBlueColor, pinkColor, purpleColor, greenColor, whiteColor, darkBlueColor]


def displayButton(frame, label, x, y, width, height, size, action):
    """Creates a new button, gives it a label a position,
    a size, a text size and binds it to the corresponding function"""
    btn = wx.Button(frame, label = label, pos = (x,y), style = wx.BORDER_NONE)
    btn.SetSize((width,height))
    btn.SetBackgroundColour(buttonColor)
    btn.SetForegroundColour(whiteColor)
    btn.SetFont(wx.Font(size, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
    frame.Bind(wx.EVT_BUTTON, action, btn)

def displayRadioButtons(button_list, x, y):
    """Displays all 6 radio buttons of the same group,
    giving them the right color and position"""
    for i in range (6):
        button_list[i].SetPosition((x, y))
        button_list[i].SetBackgroundColour(rectangleColor)
        x += 40

def displayText(frame, label, x, y, size):
    """Displays a static text at a given position and with a given size and label"""
    text = wx.StaticText(frame, label = label, pos = (x, y), style = wx.ALIGN_CENTER)
    text.SetFont(wx.Font(size,wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
    text.SetForegroundColour(whiteColor)
    if size == 12 or size == 30 or size == 21:
        text.SetBackgroundColour(rectangleColor)

def setupButton(btn, width, height, size):
    """Takes an already existing button and gives it the right box size, font size and colors"""
    btn.SetSize((width,height))
    if size == 29:
        btn.SetBackgroundColour(backgroundColor)
    else:
        btn.SetBackgroundColour(buttonColor)
    btn.SetForegroundColour(whiteColor)
    btn.SetFont(wx.Font(size, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))

def setupTextControl(player):
    """Takes an already existing text control and gives it the default size, font, and colors
    It also sets a maximum length of 14, so that the text doesn't go out of the rectangle"""
    player.SetSize((150,25))
    player.SetFont(wx.Font(13,wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
    player.SetBackgroundColour(rectangleColor)
    player.SetForegroundColour(whiteColor)
    wx.TextCtrl.SetMaxLength(player, 14)

def setupTextInCenter(text, size, boxSize):
    """Takes an already existing static text and sets it in the middle of a given area"""
    text.SetFont(wx.Font(size,wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
    text.SetSize((boxSize, -1))
    text.SetBackgroundColour(rectangleColor)
    text.SetForegroundColour(whiteColor)

def drawRectangle(x, y, width, height, dc):
    """Draws a rectangle with the given position and size"""
    dc.SetPen(wx.Pen("white", 2))
    dc.SetBrush(wx.Brush(rectangleColor, wx.BRUSHSTYLE_SOLID))
    dc.DrawRoundedRectangle(x, y, width, height, 15)

def drawOneCircle(x, y, size, border, color, dc):
    """Draws a circle with the given position, size, border and inside colors"""
    dc.SetBrush(wx.Brush(color, wx.BRUSHSTYLE_SOLID))
    dc.SetPen(wx.Pen(border, 2))
    dc.DrawCircle(x, y, size)

def drawCircles(x, y, size, spacing, dc):
    """Draws all 6 colored circles at the same time with a given start position,
    size and spacing between the circles"""
    dc.SetPen(wx.Pen(None, 0))
    for i in allMarbleColors:
        dc.SetBrush(wx.Brush(i, wx.BRUSHSTYLE_SOLID))
        dc.DrawCircle(x, y, size)
        x += spacing

def drawLine(frame, x, y):
    """Draws a horizontal line at a given position"""
    wx.StaticLine(frame, style=wx.LI_HORIZONTAL, size = (150,2), pos = (x,y))
