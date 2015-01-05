import wxversion
wxversion.select('2.8')
import wx

labels = "one two three four five six seven eight nine".split()
class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "StaticBoxSizer Test")
        self.panel = wx.Panel(self)
        box1 = self.MakeStaticBoxSizer("Box 1", labels[0:3])
        box2 = self.MakeStaticBoxSizer("Box 2", labels[3:6])
        box3 = self.MakeStaticBoxSizer("Box 3", labels[6:9])
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(box1, 0, flag=wx.EXPAND)
        sizer.Add(box2, 0, flag=wx.EXPAND)
        sizer.Add(box3, 0, flag=wx.EXPAND)
        self.panel.SetSizer(sizer)
        sizer.Fit(self)
    def MakeStaticBoxSizer(self, boxlabel, itemlabels):
        box = wx.StaticBox(self.panel, -1, boxlabel)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        for item in itemlabels:
            bw = wx.Button(self.panel, label=item)
            sizer.Add(bw, 0,flag=wx.EXPAND)
        return sizer
app = wx.PySimpleApp()
TestFrame().Show()
app.MainLoop()
