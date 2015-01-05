#!/usr/bin/env python
#coding=utf-8

import cStringIO
import base64
import re
import datetime
import wx
import os
from ConfigParser import ConfigParser 
import thread
import sys
import cPickle


class deliver_tool(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,   
                          parent=None,   
                          id=-1,   
                          title="deliver tool",   
                          pos=wx.DefaultPosition,  
                          size=(600,400),  
                          #style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER |wx.MAXIMIZE_BOX),  
                          name="mainFrame"  
                          )

        bkg=wx.Panel(self)
        self.config_file = ConfigParser()

        self.deliver_file_text = wx.TextCtrl(bkg)
        selt.deliver_file_button = wx.

        


class deliver_app(wx.App):  
    def OnInit(self):  
        self.mainFrame = deliver_tool()  
        self.mainFrame.Show()
        self.SetTopWindow(self.mainFrame)  
        return True  
  
if __name__ == "__main__":  
    mail_app = deliver_app()  
    mail_app.MainLoop()  
