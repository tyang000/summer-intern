#!/usr/bin/env python
#coding=utf-8 
import Queue
import threading
import time
import md5
import os
queue=Queue.Queue()

class WorkManager(object):
    def __init__(self, listl,thread_num=2):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue(listl)
        self.__init_thread_pool(thread_num)

    """
        初始化线程
    """
    def __init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

    """
        初始化工作队列
    """
    def __init_work_queue(self, listl):
        for i in range(len(listl[0])):
            newlist=(listl[0][i],)+listl[1:]
            self.add_job(do_job, newlist)

    """
        添加一项工作入队
    """
    def add_job(self, func, *args):
        self.work_queue.put((func, args))#任务入队，Queue内部实现了同步机制


    """
        等待所有线程运行完毕
    """   
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        #死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                do, args = self.work_queue.get(block=False)#任务异步出队，Queue内部实现了同步机制
                do(args)
                self.work_queue.task_done()#通知系统任务完成
            except:
                break

        
def do_job(args):
    dictionary =args[0][1]
    print 'checking '+dictionary[args[0][0]]+'.....'
    try:
        K=args[0][2]
        #newL=md5.getmd5list(K,args[0][0],10)
        newL=md5.md5sum2(args[0][0])
        stdL=args[0][3]
        list1=[dictionary[args[0][0]],args[0][0],[]]
        
        for m in range(len(stdL[0])):
            
            if stdL[0][m] == newL[0][m]:
                pass
            else:
                if newL[0][m] == '' or newL[0][m]==[]:
                    try:
                        list1[2].append(K[m]+'\n 不存在'.decode('utf-8','ignore')+' 主机文件大小:'.decode('utf-8','ignore')+stdL[1][m])
                    except:
                        list1[2].append(K[m].decode('GBK','ignore')+'\n 不存在'.decode('utf-8','ignore')+' 主机文件大小:'.decode('utf-8','ignore')+stdL[1][m])
                else:
                    try:
                        list1[2].append(K[m]+'\n 不匹配'.decode('utf-8','ignore')+' 主机文件大小:'.decode('utf-8','ignore')+stdL[1][m]+ ' 目标机器文件大小:'.decode('utf-8','ignore')+newL[1][m])
                    except:
                        list1[2].append(K[m].decode('GBK','ignore')+'\n 不匹配'.decode('utf-8','ignore')+' 主机文件大小:'.decode('utf-8','ignore')+stdL[1][m]+ ' 目标机器文件大小:'.decode('utf-8','ignore')+newL[1][m])
        queue.put(list1)
        print dictionary[args[0][0]]+' complete checking.'
    except KeyError:
        print dictionary[args[0][0]]+' checking failed.'
        list1=[dictionary[args[0][0]]+' 连接失败'.decode('utf-8','ignore'),args[0][0],[]]
        queue.put(list1)


def getqueue(IpList,thread):
    work_manager =  WorkManager(IpList,thread)
    work_manager.wait_allcomplete()
    return queue


