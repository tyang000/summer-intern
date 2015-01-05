#!/usr/bin/env python 
#coding=utf-8        

import md5
import Queue
import threading
import time
import sys
global f
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
        for ip in listl:
            self.add_job(do_job, ip)

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
        

#具体要做的任务
def do_job(args):
    newL=md5.md5sum(args[0])
    for m in range(len(stdL)):
            if stdL[m] in newL:
                pass
            else:
                print >>f, "file", K[m],"has error in work station with ip:", args

if __name__ == '__main__':
    L=md5.getstation()
    stdL=md5.md5sum(md5.localip())
    K=md5.getfile()
    start = time.time()
    f=open('output.txt','w')
    work_manager =  WorkManager(L, 10)
    work_manager.wait_allcomplete()
    end = time.time()
    print >> f, "cost all time: %s" % (end-start)
    f.close()
