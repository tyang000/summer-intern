#!/usr/bin/env python 
#-*- coding:GB2312 -*-    
import os
import socket
import sys
import paramiko
import Queue
import threading
import time
import os
queue=Queue.Queue()
import sys
reload(sys)
sys.setdefaultencoding( "GB2312" )
def getfile():
    "read the checklist"
    File=open('checklist.ini')
    checklist=File.readlines()
    for i in range(len(checklist)):
        checklist[i]=checklist[i].strip()
    f=open('directory.ini')
    directory=f.readlines()
    for i in range(len(directory)):
        directory[i] = directory[i].strip()
        filenames=os.listdir(os.path.expanduser('~')+'/'+directory[i])
        for m in range(len(filenames)):
            if directory[i]=='':
                filenames[m]=directory[i]+filenames[m]
            else:
                filenames[m]=directory[i]+'/'+filenames[m]
            if os.path.isfile(os.path.expanduser('~')+'/'+filenames[m]):
                pass
            else:
                filenames[m]=''
            if ' 'in filenames[m]:
                print filenames[m]+ ' :  文件名中有空格，请修改后重试'.decode('GB2312','ignore')
                filenames[m]=''
        checklist += filenames
    return checklist

def getfile2():
    "read the checklist"
    File=open('checklist.ini')
    checklist=File.readlines()
    for i in range(len(checklist)):
        checklist[i]=checklist[i].strip()
    f=open('directory.ini')
    directory=f.readlines()
    for i in range(len(directory)):
        directory[i] = directory[i].strip()
        filenames=os.listdir(os.path.expanduser('~')+'/'+directory[i])
        for m in range(len(filenames)):
            if directory[i]=='':
                filenames[m]=directory[i]+filenames[m]
            else:
                filenames[m]=directory[i]+'/'+filenames[m]
            if os.path.isfile(os.path.expanduser('~')+'/'+filenames[m]):
                pass
            else:
                filenames[m]=''
            if ' 'in filenames[m]:
                filenames[m]=''
        checklist += filenames
    return checklist

def localip():
    myname=socket.getfqdn(socket.gethostname())
    myaddr=socket.gethostbyname(myname)
    return myaddr

def newgetstation():
    host=open('/etc/hosts')
    x=host.readlines()
    k=[]
    finalstation=[]
    for i in range(len(x)):
        x[i]=x[i].rstrip().split()
        try:
            if x[i][0] == '#' or x[i][0][0]=='#' or x[i][0]=='127.0.0.1':
                pass
            else:
                k.append(x[i][0]+' '+x[i][1])
        except:
            pass
    for i in range(len(k)):
        if k[i] in finalstation:
            pass
        else:
            finalstation.append(k[i])
    return finalstation

def getstation():
    "get station name list"
    host=open('/etc/hosts')
    x=host.readlines()
    k=[]
    L=[]
    for i in range(len(x)):
        x[i]=x[i].rstrip().split()
        try:
            if x[i][0] == '#' or x[i][0][0]=='#':
                pass
            else:
                k.append(x[i][0])
        except:
            pass
    for i in range(len(k)):
        if k[i] in L:
            pass
        else:
            L.append(k[i])
    L.remove('127.0.0.1')
    L.remove(localip())
    return L

def matchdict():
    host=open('/etc/hosts')
    x=host.readlines()
    d={}
    for i in range(len(x)):
        x[i]=x[i].rstrip().split()
        try:
            if x[i][0] == '#'or x[i][0][0]=='#':
                pass
            else:
                d[x[i][0]]=x[i][1]
        except:
            IndexError
    return d

def matchdict2():
    host=open('/etc/hosts')
    x=host.readlines()
    d={}
    for i in range(len(x)):
        x[i]=x[i].rstrip().split()
        try:
            if x[i][0] == '#' or x[i][0][0]=='#':
                pass
            else:
                for m in range(1,len(x[i])):
                    d[x[i][m]]=x[i][0]
        except:
            IndexError
    return d

def comparemd5():
    "compare whether the other work stations' files are consensus to the checklist"
    if checkfile2():
        stdlist=md5sum(localip())
    else:
        print "Checklist has error, please check."
    k=[]
    L=getstation()
    errornum=0
    for i in range(len(L)):
        k.append(md5sum(L[i]))
    for m in range(len(stdlist)):
        for n in range(len(k)):
            if stdlist[m] in k[n]:
                pass
            else:
                errornum +=1
                print "file", getfile()[m],"has error in work station with ip:", L[n]
    if errornum ==0:
        print "Everything is fine, congratulations!"
      
    
def checkfile():
    "check whether the file in checklist is in the local host"
    F=open('checklist.ini')
    x=F.readlines()
    for i in range(len(x)):
        x[i]=x[i].rstrip().split('/')
    return x

def checkfile2():
    "check whether the file in checklist is in the local host"
    a=0
    path=os.getcwd()
    L=checkfile()
    for i in range(len(L)):
        newpath=path+'/'+L[i][0]
        if L[i][1] in os.listdir(newpath):
            pass
        else:
            a+=1
    if a ==0:
        return True
    else:
        return False


####################################################

class WorkManager2(object):
    def __init__(self, files, ping,thread_num=2):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.file = files
        self.__init_work_queue(self.file,ping)
        self.__init_thread_pool(thread_num)

    """
        初始化线程
    """
    def __init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work2(self.work_queue))

    """
        初始化工作队列
    """
    def __init_work_queue(self, files, ping):
        for file in files:
            self.add_job(md5sum, file, ping)

    """
        添加一项工作入队
    """
    def add_job(self, func, file, ping):
        self.work_queue.put((func, file, ping))#任务入队，Queue内部实现了同步机制


    """
        等待所有线程运行完毕
    """   
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

class Work2(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        #死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                do, file, ping = self.work_queue.get(block=False)#任务异步出队，Queue内部实现了同步机制
                do(file, ping)
                self.work_queue.task_done()#通知系统任务完成
            except:
                break

def md5sum(file,ping):
    "calculate the md5 value for the local host files in the checklist"
    md5value=''
    usr_home = os.path.expanduser('~')
    file=file.rstrip()
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ping,timeout=3.0)
    cmd="md5sum "+usr_home+'/'+file
    stdin, stdout, stderr = s.exec_command(cmd)
    md5value=stdout.read()
    try:
        md5value=md5value.split()[0]
    except:
        md5value=''
    stdin1, stdout1, stderr1=s.exec_command('ls -lh '+usr_home+'/'+file)
    try:
        filesize=stdout1.read().split()[4]
        if filesize[-1] in '0123456789':
            filesize ='1k'
    except:
        filesize=''
    queue.put([file,md5value,filesize])

def getmd5list(files,ping,thread):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        s.connect(ping,timeout=3.0)
    except:
        raise KeyError
    work_manager = WorkManager2(files,ping,thread)
    work_manager.wait_allcomplete()
    md5filevaluelist=[]
    md5list=[]
    filesizelist=[]
    dict={}
    dict2={}
    while queue.qsize()>0:
        md5filevaluelist.append(queue.get())
    for i in range(len(md5filevaluelist)):
        dict[md5filevaluelist[i][0]]=md5filevaluelist[i][1]
    for i2 in range(len(md5filevaluelist)):
        dict2[md5filevaluelist[i2][0]]=md5filevaluelist[i2][2]
    for m in range(len(files)):
        try:
            md5list.append(dict[files[m].rstrip()])
        except:
            md5list.append('')
    for n in range(len(files)):
        try:
            filesizelist.append(dict2[files[n].rstrip()])
        except:
            filesizelist.append('')
    return md5list,filesizelist

def md5sum2(ping):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        s.connect(ping,timeout=3.0)
    except:
        raise KeyError
    usr_home = os.path.expanduser('~')
    files=getfile2()
    md5_valuelist=[]
    filesizelist=[]
    for i in range(len(files)):
        files[i]=files[i].strip()
        cmd="md5sum "+usr_home+'/'+files[i]

        stdin, stdout, stderr = s.exec_command("md5sum "+usr_home+'/'+files[i])
        try:
            md5value = stdout.read().split()[0]
        except:
            md5value = ''
        
        md5_valuelist.append(md5value)
        stdin1, stdout1, stderr1=s.exec_command('ls -lh '+usr_home+'/'+files[i])
        try:
            filesize=stdout1.read().split()[4]
            if filesize[-1] in '0123456789':
                filesize ='1k'
        except Exception as e:
            filesize=''
        filesizelist.append(filesize)
    return md5_valuelist,filesizelist

if __name__=='__main__':
    print md5sum2('192.1.101.231')
    #print localip()
    #newgetstation()
    #print getmd5list(getfile(),'10.144.118.241',10)
