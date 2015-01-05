#!/bin/env python
import wxversion
wxversion.select('2.8')
import wx
class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(parent=None, title='Bare')
        frame.Show()
        return True
app = App()
app.MainLoop()
