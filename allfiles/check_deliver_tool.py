#!/usr/bin/env python
#coding=utf-8
import wx
import wx.grid
import wx.html
import md5
import os
import Queue
import threading
import time
import tool_check
import tool_deliver
import paramiko
import ConfigParser
import scp
import logging
from difflib import *
import webbrowser

def getwork1(IpList,thread=2):
    queue=tool_check.getqueue(IpList,thread)
    return queue

def getwork2(filepath, stations, thread=2):
    queue=tool_deliver.getqueue(filepath,stations,thread)
    return queue
                
class InsertFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "易工程化检测工具".decode('utf-8','ignore'),size=(700,550))
        nb = wx.Notebook(self)
        #panel1
        self.panel = wx.Panel(nb)
        #main sizer on First page
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        #start button
        self.button = wx.Button(self.panel, label="开始检测".decode('utf-8','ignore'),size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.button)
        self.sizer.Add((20,20),1)
        #First Horizontal sizer
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add((20,20),1)
        sizer1.Add(self.button,1,wx.EXPAND)
        sizer1.Add((20,20),1)
        self.sizer.Add(sizer1,0,wx.EXPAND|wx.ALL,5)
        #StaticLine
        self.sizer.Add(wx.StaticLine(self.panel), 0,wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        self.sizer.Add((20,20),0.2)
        #ListBox__work sation
        self.listBox = wx.ListBox(self.panel, -1,(50,111),(150,300),[],wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.OnListClick, self.listBox)
        #Second Horizontal sizer
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        #Vertical sizer in Second Horizontal sizer
        sizer3 = wx.BoxSizer(wx.VERTICAL)
        hostlb = wx.StaticText(self.panel, -1, "工作站".decode('utf-8','ignore'))
        sizer3.Add(hostlb, 0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL,5)
        sizer3.Add(self.listBox,0,wx.EXPAND|wx.ALL, 10)
        self.sizer2.Add(sizer3,5,wx.EXPAND|wx.ALL, 10)
        self.sizer2.Add((20,20),1)
        #ListBox_Problematic File
        self.problistBox = wx.ListBox(self.panel, -1,(225,111),(150,300),[],wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListClick2, self.problistBox)
        #popup menu
        self.popupmenu=wx.Menu()
        compare=self.popupmenu.Append(-1,"比对文件".decode('utf-8','ignore'))
        self.Bind(wx.EVT_MENU,self.OnMenuSelect,compare)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopMenu, self.problistBox)
        #Second Vertical sizer in Second Horizontal sizer
        sizer4 = wx.BoxSizer(wx.VERTICAL)
        listlb = wx.StaticText(self.panel, -1, "问题文件".decode('utf-8','ignore'))
        sizer4.Add(listlb, 0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL,5)
        sizer4.Add(self.problistBox,0,wx.EXPAND|wx.ALL, 10)
        self.sizer2.Add(sizer4,5,wx.EXPAND|wx.ALL, 10)
        #Second Horizontal sizer complete
        self.sizer.Add(self.sizer2,0,wx.EXPAND|wx.ALL, 10)
        self.sizer.Add((20,20),4)
        self.panel.SetSizer(self.sizer)
        self.panel.Fit()
        #add the notebook page
        nb.AddPage(self.panel,"全站检测".decode('utf-8','ignore'))
        
        #panel2
        self.panel2 = wx.Panel(nb)
        #main sizer on Second page
        self.sizer_2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_2.Add((20,20),1)
        #GetGourp Button, Choose File Button, Execute Button
        #self.button_2 = wx.Button(self.panel2, label="获取分组".decode('utf-8','ignore'),size=(80, 40))
        #self.Bind(wx.EVT_BUTTON, self.OnButton2, self.button_2)
        self.button_3 = wx.Button(self.panel2, label="浏览".decode('utf-8','ignore'),size=(60, 25))
        self.Bind(wx.EVT_BUTTON, self.OnButton3, self.button_3)
        self.button_4 = wx.Button(self.panel2, label="开始复制".decode('utf-8','ignore'),size=(80, 40))
        self.Bind(wx.EVT_BUTTON, self.OnButton4, self.button_4)
        #First Horizontal sizer
        sizer1_2 = wx.BoxSizer(wx.HORIZONTAL)
        #sizer1_2.Add((20,20),1)
        #sizer1_2.Add(self.button_2,2,wx.EXPAND)
        sizer1_2.Add((20,20),1)
        sizer1_2.Add(self.button_4,2,wx.EXPAND)
        sizer1_2.Add((20,20),1)
        self.sizer_2.Add(sizer1_2,0, wx.EXPAND|wx.ALL, 10)
        fileLabel = wx.StaticText(self.panel2, -1, "文件".decode('utf-8','ignore'))
        self.fileText = wx.TextCtrl(self.panel2, -1, "",size=(250, -1))
        sizer1_1_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1_1_2.Add((20,20),1)
        sizer1_1_2.Add(fileLabel)
        sizer1_1_2.Add(self.fileText,10,wx.EXPAND)
        sizer1_1_2.Add(self.button_3)
        sizer1_1_2.Add((20,20),1)
        self.sizer_2.Add(sizer1_1_2,0, wx.EXPAND|wx.ALL, 10)
        
        #static line
        self.sizer_2.Add(wx.StaticLine(self.panel2), 0,wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        #First listbox_groups
        self.SectionBox = wx.ListBox(self.panel2, -1,(50,111),(150,300),[],wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.OnSectionListClick, self.SectionBox)
        #Second Horizontal sizer
        self.sizer2_2 = wx.BoxSizer(wx.HORIZONTAL)
        #First Vertical sizer in Second Horizontal sizer
        sizer3_2 = wx.BoxSizer(wx.VERTICAL)
        Sectionlb = wx.StaticText(self.panel2, -1, "工作组".decode('utf-8','ignore'))
        sizer3_2.Add(Sectionlb, 0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL,5)
        sizer3_2.Add(self.SectionBox,0,wx.EXPAND|wx.ALL, 10)
        self.sizer2_2.Add(sizer3_2,5,wx.EXPAND|wx.ALL, 10)
        self.sizer2_2.Add((20,20),1)
        #Second Listbox_work stations
        self.StationBox = wx.ListBox(self.panel2, -1,(225,111),(150,300),[],wx.LB_SINGLE)
        #Second Vertical sizer in Second Horizontal sizer
        sizer4_2 = wx.BoxSizer(wx.VERTICAL)
        Stationlb = wx.StaticText(self.panel2, -1, "工作站".decode('utf-8','ignore'))
        sizer4_2.Add(Stationlb, 0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL,5)
        sizer4_2.Add(self.StationBox,0,wx.EXPAND|wx.ALL, 10)
        self.sizer2_2.Add(sizer4_2,5,wx.EXPAND|wx.ALL, 10)
        #Second Horizontal sizer complete
        self.sizer_2.Add(self.sizer2_2,0,wx.EXPAND|wx.ALL, 10)
        self.sizer_2.Add((20,20),4)
        self.panel2.SetSizer(self.sizer_2)
        self.panel2.Fit()
        #add panel2 to the second page of the notebook
        nb.AddPage(self.panel2,"分组整理".decode('utf-8','ignore'))

        self.panel3 = wx.Panel(nb)
        Sizer=wx.BoxSizer(wx.VERTICAL)
        Sizer.Add((20,20),1)
        timeButton=wx.Button(self.panel3, label="检测时间是否同步".decode('utf-8','ignore'),size=(120, 50))
        self.Bind(wx.EVT_BUTTON,self.OntimeButton,timeButton)
        Sizer2_0=wx.BoxSizer(wx.HORIZONTAL)
        Sizer2_0.Add((20,20),1)
        Sizer2_0.Add(timeButton)
        Sizer2_0.Add((20,20),1)
        Sizer.Add(Sizer2_0,0,wx.EXPAND|wx.ALL,10)
        Sizer_1=wx.BoxSizer(wx.HORIZONTAL)
        self.SectionBox2 = wx.ListBox(self.panel3, -1,(50,111),(100,300),[],wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.OnSectionClick, self.SectionBox2)
        Sizer3_2 = wx.BoxSizer(wx.VERTICAL)
        Sectionlb = wx.StaticText(self.panel3, -1, "工作站".decode('utf-8','ignore'))
        Sizer3_2.Add(Sectionlb, 0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL,5)
        Sizer3_2.Add(self.SectionBox2,0,wx.EXPAND|wx.ALL, 10)
        Sizer_1.Add(Sizer3_2,5,wx.EXPAND|wx.ALL, 10)
        Sizer_1.Add((20,20),1)
        self.StationBox2 = wx.grid.Grid(self.panel3, -1,(175,111),(200,300))
        self.StationBox2.CreateGrid(6,6)
        self.StationBox2.SetColSize(5,350)
        Sizer4_2 = wx.BoxSizer(wx.VERTICAL)
        Stationlb = wx.StaticText(self.panel3, -1, "硬盘信息".decode('utf-8','ignore'))
        Sizer4_2.Add(Stationlb, 0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL,5)
        Sizer4_2.Add(self.StationBox2,0,wx.EXPAND|wx.ALL, 10)
        Sizer_1.Add(Sizer4_2,10,wx.EXPAND|wx.ALL, 10)
        Sizer.Add(Sizer_1,0,wx.EXPAND|wx.ALL,10)
        Sizer.Add((20,20),1)
        self.panel3.SetSizer(Sizer)
        self.panel3.Fit()

        
        self.panel4 = wx.Panel(nb)
        newSizer=wx.BoxSizer(wx.VERTICAL)
        newSizer.Add((20,20),1)
        Sizer_0=wx.BoxSizer(wx.HORIZONTAL)
        PidButton=wx.Button(self.panel4, label="终止进程".decode('utf-8','ignore'),size=(60, 25))
        PidLabel = wx.StaticText(self.panel4, -1, "PID:")
        self.fileText2 = wx.TextCtrl(self.panel4, -1, "",size=(250, -1))
        Sizer_0.Add((20,20),1)
        Sizer_0.Add(PidLabel)
        Sizer_0.Add(self.fileText2)
        Sizer_0.Add(PidButton)
        Sizer_0.Add((20,20),1)
        self.Bind(wx.EVT_BUTTON,self.OnPidButton,PidButton)
        newSizer.Add(Sizer_0,0,wx.EXPAND|wx.ALL,10)
        newSizer_1=wx.BoxSizer(wx.HORIZONTAL)
        self.SectionBox3 = wx.ListBox(self.panel4, -1,(50,111),(150,300),[],wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.OnSectionClick2, self.SectionBox3)
        newSizer3_2 = wx.BoxSizer(wx.VERTICAL)
        Sectionlb = wx.StaticText(self.panel4, -1, "工作站".decode('utf-8','ignore'))
        newSizer3_2.Add(Sectionlb, 0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL,5)
        newSizer3_2.Add(self.SectionBox3,0,wx.EXPAND|wx.ALL, 10)
        newSizer_1.Add(newSizer3_2,5,wx.EXPAND|wx.ALL, 10)
        newSizer_1.Add((20,20),1)
        self.StationBox3 = wx.grid.Grid(self.panel4, -1,(225,111),(150,300))
        self.StationBox3.CreateGrid(6,11)
        self.StationBox3.SetColSize(10,350)
        newSizer4_2 = wx.BoxSizer(wx.VERTICAL)
        Stationlb = wx.StaticText(self.panel4, -1, "进程信息".decode('utf-8','ignore'))
        newSizer4_2.Add(Stationlb, 0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL,5)
        newSizer4_2.Add(self.StationBox3,0,wx.EXPAND|wx.ALL, 10)
        newSizer_1.Add(newSizer4_2,10,wx.EXPAND|wx.ALL, 10)
        newSizer.Add(newSizer_1,0,wx.EXPAND|wx.ALL,10)
        newSizer.Add((20,20),1)
        self.panel4.SetSizer(newSizer)
        self.panel4.Fit()


        nb.AddPage(self.panel3,"时间与硬盘管理".decode('utf-8','ignore'))
        nb.AddPage(self.panel4,"进程管理".decode('utf-8','ignore'))
        
        self.OnButton2(None)
        
    def OntimeButton(self,event):
        localtime=os.popen("date '+%T %D'").read()
        start=time.time()
        localtime=localtime.split()
        localtime[0]=localtime[0].split(':')
        localsectime=int(localtime[0][0])*3600+int(localtime[0][1])*60+int(localtime[0][2])

        ipvalue=md5.newgetstation()
        outputstring=''
        for i in range(len(ipvalue)):
            try:
                print 'checking '+ipvalue[i]
                s=paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                s.connect(ipvalue[i].split()[0],timeout=3.0)
                stdin1, stdout1, stderr1=s.exec_command("date '+%T %D'")
                end=time.time()
                remotetime=stdout1.read()
                remotetime=remotetime.split()
                remotetime[0]=remotetime[0].split(':')
                remotesectime=int(remotetime[0][0])*3600+int(remotetime[0][1])*60+int(remotetime[0][2])-int(end-start)
                if remotetime[1]==localtime[1] and abs(remotesectime-localsectime)<=10:
                    outputstring+=ipvalue[i]+' 时间正确\n'.decode('utf-8','ignore')
                elif remotetime[1]!=localtime[1]:
                    outputstring+=ipvalue[i]+' 日期不匹配\n'.decode('utf-8','ignore')
                elif remotesectime-localsectime>10:
                    outputstring+=ipvalue[i]+' 快了'.decode('utf-8','ignore')+str(remotesectime-localsectime)+'秒\n'.decode('utf-8','ignore')
                elif remotesectime-localsectime<-10:
                    outputstring+=ipvalue[i]+' 慢了'.decode('utf-8','ignore')+str(localsectime-remotesectime)+'秒\n'.decode('utf-8','ignore')
            except:
                outputstring+=ipvalue[i]+' 无法连接\n'.decode('utf-8','ignore')
        f=open('timediff.txt','w')
        f.write(outputstring.encode('GB2312','ignore'))
        f.close()
        dlg = wx.MessageDialog(None,outputstring,"提醒".decode('utf-8','ignore'),wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        

    def OnPidButton(self,event):
        #终止进程
        ipvalue=self.SectionBox3.GetStringSelection()
        Pid=self.fileText2.GetValue()
        try:
            s=paramiko.SSHClient()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.connect(ipvalue.split()[0],timeout=3.0)
            cmd = 'kill -9 '+Pid
            print cmd
            stdin1, stdout1, stderr1=s.exec_command(cmd)
        except:
            dlg1 = wx.MessageDialog(None,ipvalue+' 连接失败'.decode('utf-8','ignore'),"提醒".decode('utf-8','ignore'),wx.OK|wx.ICON_INFORMATION)
            dlg1.ShowModal()
            
    def OnSectionClick(self,event):
        #硬盘管理
        a=''
        ipvalue=self.SectionBox2.GetStringSelection()
        collabel=['文件系统'.decode('utf-8','ignore'),'容量'.decode('utf-8','ignore'),'已用'.decode('utf-8','ignore'),'可用'.decode('utf-8','ignore'),'已用%'.decode('utf-8','ignore'),'挂载点'.decode('utf-8','ignore')]
        try:
            s=paramiko.SSHClient()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.connect(ipvalue.split()[0],timeout=3.0)
            stdin1, stdout1, stderr1=s.exec_command('df -lh')
            a=stdout1.read()
            a=a.split()
            if len(a)/6>self.StationBox2.GetNumberRows()+1:
                self.StationBox2.AppendRows(numRows=len(a)/6-self.StationBox2.GetNumberRows()-1)
                
            elif len(a)/6<self.StationBox2.GetNumberRows()+1:
                self.StationBox2.DeleteRows(numRows=self.StationBox2.GetNumberRows()+1-len(a)/6)
                
            for i in range(6):
                self.StationBox2.SetColLabelValue(i, collabel[i])
                for m in range(len(a)/6-1):
                    self.StationBox2.SetCellValue(m,i,a[6+6*m+i])
        except:
            for x in range(self.StationBox2.GetNumberRows()):
                for y in range(self.StationBox2.GetNumberCols()):
                    self.StationBox2.SetCellValue(x,y,' ')

            dlg1 = wx.MessageDialog(None,ipvalue+' 连接失败'.decode('utf-8','ignore'),"提醒".decode('utf-8','ignore'),wx.OK|wx.ICON_INFORMATION)
            dlg1.ShowModal()

        
    def OnSectionClick2(self,event):
        #进程管理
        a=''
        ipvalue=self.SectionBox3.GetStringSelection()
        collabel=['User','PID','%CPU','%MEM','VSZ','RSS','TTY','STAT','START','TIME','COMMAND']
        try:
            s=paramiko.SSHClient()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.connect(ipvalue.split()[0],timeout=3.0)
            stdin1, stdout1, stderr1=s.exec_command('ps u --sort %cpu')
            a=stdout1.readlines()
            if len(a)==1:
                raise IndexError      
            else:
                for index in range(len(a)):
                    a[index]=a[index].strip().split()
                    if len(a[index])>11:
                        for index3 in range(11,len(a[index])):
                            a[index][10]+=' '+a[index][index3]
                if len(a)>(self.StationBox3.GetNumberRows()+1):
                    self.StationBox3.AppendRows(numRows=len(a)-self.StationBox3.GetNumberRows()-1)
                    
                elif len(a)<(self.StationBox3.GetNumberRows()+1):
                    self.StationBox3.DeleteRows(numRows=self.StationBox3.GetNumberRows()+1-len(a))
                    
                for i in range(11):
                    self.StationBox3.SetColLabelValue(i, collabel[i])
                    for m in range(len(a)-1):
                            self.StationBox3.SetCellValue(m,i,a[m+1][i])

        except:
            for x in range(self.StationBox3.GetNumberRows()):
                for y in range(self.StationBox3.GetNumberCols()):
                    self.StationBox3.SetCellValue(x,y,' ')
            if len(a)==1:
                dlg1 = wx.MessageDialog(None,ipvalue+' 没有运行的用户进程'.decode('utf-8','ignore'),"提醒".decode('utf-8','ignore'),wx.OK|wx.ICON_INFORMATION)
                dlg1.ShowModal()
            else:
                dlg1 = wx.MessageDialog(None,ipvalue+' 连接失败'.decode('utf-8','ignore'),"提醒".decode('utf-8','ignore'),wx.OK|wx.ICON_INFORMATION)
                dlg1.ShowModal()
       
    def OnButton2(self,event):
        #Autostart
        
        self.conf=ConfigParser.ConfigParser()
        self.conf.read('config.ini')
        self.sections=self.conf.sections()
        self.SectionBox.Set(self.sections)

        stations=md5.newgetstation()
        self.SectionBox2.Set(stations)
        self.SectionBox3.Set(stations)
        
        
    
    def OnButton3(self, event):
        #bind to choose file button on page 2
        wildcard = "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "请选择文件".decode('utf-8','ignore'), os.getcwd(),"", wildcard, wx.OPEN|wx.MULTIPLE)
        retcode=dialog.ShowModal()  
        if (retcode == wx.ID_OK):
            self.fileText.Clear()
            for file in dialog.GetPaths():
                self.fileText.AppendText(file+';')
            self.filepath=dialog.GetPaths()
        dialog.Destroy()

    def OnButton4(self, event):
        #bind to copy file button on page 2
        f=open('authorization.ini').readlines()
        ips=''
        for ip in f:
            ips += ip
        if md5.localip() in ips:
            pass
        else:
            dlg0 = wx.MessageDialog(None,"该主机没有权限分发文件，如需要赋予权限请在authorization.ini中添加！".decode('utf-8','ignore'),"提醒".decode('utf-8','ignore'),wx.OK|wx.ICON_INFORMATION)
            dlg0.ShowModal()
            raise SyntaxError
        
        filepath = []
        self.filepath = self.fileText.GetValue()
        self.filepath = self.filepath.split(';')
        self.filepath = self.filepath[:-1]
        for i in range(len(self.filepath)):
            try:
                if self.filepath[i][0]=='/':
                    pass
                else:
                    self.filepath[i]=os.path.expanduser('~')+'/'+self.filepath[i]
            except:
                pass
            if ' ' in self.filepath[i]:
                print self.filepath[i]+  ' :  文件名中有空格，请修改后重试'.decode('utf-8','ignore')
            elif os.popen('ls -lh '+self.filepath[i].encode('GBK')).read()[0].split()[0] == 'l':
                print os.popen('ls -lh '+self.filepath[i].encode('GBK')).read()
                print self.filepath[i]+  ' 是link文件，不能分发'.decode('utf-8','ignore')
            else:
                filepath.append(self.filepath[i])

        a=0
        filetext=''
        options=[]
        options1=[]
        alertstring=''
        dictionary=md5.matchdict2()
        for i in range(len(self.options)):
            try:
                if dictionary[self.options[i]] == md5.localip():
                    pass
                else:
                    options1.append(self.options[i])
            except:
                pass
        for i in range(len(options1)):
            if options1[i] in self.options2:
                options.append(options1[i])
            else:
                pass
        for file in filepath:
            filetext += file+'\n'
        dlg = wx.MessageDialog(None, "确定复制文件： ".decode('utf-8','ignore')+filetext+' 到：'.decode('utf-8','ignore')+self.SectionBox.GetStringSelection()+'?','提醒'.decode('utf-8','ignore'),wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        retcode=dlg.ShowModal()
        if (retcode == wx.ID_OK):
            queue2=getwork2(filepath,options,10)
            if queue2.qsize() == 0:
                dlg1 = wx.MessageDialog(None,"全部工作站已成功复制指定文件！".decode('utf-8','ignore'),"提醒".decode('utf-8','ignore'),wx.OK|wx.ICON_INFORMATION)
                dlg1.ShowModal()
            else:
                while queue2.qsize() >0: 
                    alertstring += queue2.get()+'\n'
                dlg2 = wx.MessageDialog(None,"以下工作站未成功复制指定文件，请重试或检查！\n".decode('utf-8','ignore')+alertstring,"提醒".decode('utf-8','ignore'),wx.OK|wx.ICON_ERROR)
                dlg2.ShowModal()
        else:
            pass
        dlg.Destroy()

    def OnSectionListClick(self,event):
        #bind to StationList on Page 2
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sectionid=self.SectionBox.GetSelection()
        self.selectsections=self.sections[sectionid]
        self.options=self.conf.options(self.selectsections)
        self.options2=self.conf.options(self.selectsections)
        for i in range(len(self.options2)):
            try:
                s.connect(self.options2[i],timeout=3.0)
            except:
                self.options2[i] += '  connection failed'
        self.StationBox.Set(self.options2)
        
    def OnListClick(self, event):
        #bind to HostList on Page1
        self.listid1=self.listBox.GetSelection()
        self.problemlist=[]
        self.problemlist.extend(self.finallist[self.listid1][2])
        self.problistBox.Set(self.problemlist)
        
    def OnListClick2(self, event):
        #bind to FileList on Page1
        self.usr_home = os.path.expanduser('~')
        listid=self.problistBox.GetSelection()
        ping=self.finallist[self.listid1][0]
        probfile=self.problemlist[listid].split()[0]
        probfile=self.usr_home+'/'+probfile
        probfile=probfile.strip('\n')
        dlg = wx.MessageDialog(None, "确定复制文件: ".decode('utf-8','ignore')+probfile+' 到:'.decode('utf-8','ignore')+ping+'?','提醒'.decode('utf-8','ignore'),wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        retcode=dlg.ShowModal()
        if (retcode == wx.ID_OK):
            if scp.copy_file_to_host(probfile,self.finallist[self.listid1][0],22,'d5000',True)==True:
                dlg1 = wx.MessageDialog(None,"已成功复制指定文件！".decode('utf-8','ignore'),"提醒".decode('utf-8','ignore'),wx.OK|wx.ICON_INFORMATION)
                dlg1.ShowModal()
            else:
                dlg2 = wx.MessageDialog(None,"未成功复制，请重试或检查！".decode('utf-8','ignore'),"提醒".decode('utf-8','ignore'),wx.OK|wx.ICON_ERROR)
                dlg2.ShowModal()
        dlg.Destroy()
        
    def OnShowPopMenu(self, event):
        #bind to pop submenu on Page1
        pos = event.GetPosition()
        pos = self.panel.ScreenToClient(pos)
        self.panel.PopupMenu(self.popupmenu, pos)
        
    def OnMenuSelect(self,event):
        #bind to select submenu on Page1
        try:
            self.usr_home = os.path.expanduser('~')
            listid=self.problistBox.GetSelection()

            ping=self.problemlist[0]
            probfile=self.problemlist[listid].split()[0]
            probfile=self.usr_home+'/'+probfile
            probfile=probfile.strip('\n')
            scp_cmd = 'scp '+self.finallist[self.listid1][0]+":"+probfile.encode('GBK')+' '+probfile.encode('GBK')+'_2'
         
            os.popen(scp_cmd)
            local_file = open(probfile.encode('GBK'))
            a=local_file.readlines()
            remote_file = open(probfile.encode('GBK')+'_2')
            b=remote_file.readlines()

            result_lines = HtmlDiff.make_file(HtmlDiff(),a,b)

            result_file = open('diff_result.html','w')
            result_file.write(result_lines)
            
            webbrowser.open('diff_result.html')
            
            local_file.close()
            remote_file.close()
            result_file.close()
            
            os.popen('rm '+probfile.encode('GBK')+'_2')
        except Exception as e:
            print e
            dlg = wx.MessageDialog(None,"文件不存在".decode('utf-8','ignore'),"提醒".decode('utf-8','ignore'),wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
        
           
        
    def OnButton(self, event):
        #bind to start Button on Page1
        print 'checking local files...'
        self.finallist=[]
        IpList=md5.getstation()
        dictionary =md5.matchdict()
        K=md5.getfile()
        stdL=md5.getmd5list(K,md5.localip(),10)
        #stdL=md5.md5sum2(md5.localip())
        print 'local files checking complete'  
        start2 = time.time()
        a=(IpList,dictionary,K,stdL)
        queue=getwork1(a,10)
        end2 = time.time()
        print "cost all time: %s" % (end2-start2)
        while queue.qsize()>0:
            self.finallist.append(queue.get())
        self.userlist=[]
        for i in range(len(self.finallist)):
            self.userlist.append(self.finallist[i][0]+' '+self.finallist[i][1])
        self.listBox.Set(self.userlist)

              
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = InsertFrame()
    frame.Show()
    app.MainLoop()

