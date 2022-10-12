import wx
import MainMenu as mm

def main():

    app = wx.App(False)
    frame = mm.MainMenu(None)
    #The size of the frame can't be changed by user
    frame.SetMaxSize(wx.Size(1000,700))
    frame.SetMinSize(wx.Size(1000,700))
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
