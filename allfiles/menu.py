#!/usr/bin/env python
import wxversion
wxversion.select('2.8')
import wx
'''
class ToolbarFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Toolbars',
        size=(300, 200))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('White')
        statusBar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        toolbar.Realize()
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu1.Append(wx.NewId(), "Save", "Save in status bar")
        menu1.Append(wx.NewId(), "Load", "Load in status bar")
        menuBar.Append(menu1, "&File")
        menu2 = wx.Menu()
        menu2.Append(wx.NewId(), "&Copy", "Copy in status bar")
        menu2.Append(wx.NewId(), "C&ut", "")
        menu2.Append(wx.NewId(), "Paste", "")
        menu2.AppendSeparator()
        menu2.Append(wx.NewId(), "&Options...", "Display Options")
        menuBar.Append(menu2, "&Edit")
        self.SetMenuBar(menuBar)
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = ToolbarFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
'''
class MenuEventFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Menus',
        size=(300, 200))
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menuItem = menu1.Append(-1, "&Exit...")
        menuBar.Append(menu1, "&File")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnCloseMe, menuItem)
    def OnCloseMe(self, event):
        self.Close(True)
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MenuEventFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
