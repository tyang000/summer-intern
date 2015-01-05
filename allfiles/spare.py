#!/usr/bin/env python
"""Spare.py is a starting point for a wxPython program."""
import wxversion
wxversion.select('2.8')
import wx
class Frame(wx.Frame):
    pass
class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent=None, title='Spare',size=(10,10))
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
if __name__ == '__main__':
    
    app = App()
    app.MainLoop()
