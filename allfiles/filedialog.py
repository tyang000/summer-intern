#!/usr/bin/env python
#coding=utf-8
import wx
import os
if __name__ == "__main__":
    app = wx.PySimpleApp()
    #wildcard = "Python source (*.py)|*.py|"+"Compiled Python (*.pyc)|*.pyc|"+"All files (*.*)|*.*"
    #dialog = wx.FileDialog(None, "Choose a file", os.getcwd(),"", wildcard, wx.OPEN)
    #dialog2 = wx.FileSelector('message', default_path="", default_filename="",default_extension="", wildcard="*.*", flags=0, parent=None,x=-1, y=-1)
    #dialog3 = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    choices = ["Alpha", "Baker", "Charlie", "Delta"]
    dialog4 = wx.SingleChoiceDialog(None, "Pick A Word", "Choices",choices)
    dialog5 = wx.TextEntryDialog(None,"What kind of text would you like to enter?","Text Entry", "Default Value", style=wx.OK|wx.CANCEL)
    dialog4.ShowModal()
