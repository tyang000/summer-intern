#!/usr/bin/env python
#coding=utf-8 
import Queue
import threading
import time
import md5
import scp
import os
queue2=Queue.Queue()

class WorkManager2(object):
    def __init__(self, filepath, stations,thread_num=2):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.file = filepath
        self.__init_work_queue(self.file,stations)
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
    def __init_work_queue(self, filepath, stations):
        for station in stations:
            self.add_job(do_job2, filepath, station)

    """
        添加一项工作入队
    """
    def add_job(self, func, filepath, station):
        self.work_queue.put((func, filepath, station))#任务入队，Queue内部实现了同步机制


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
                do, filepath, station = self.work_queue.get(block=False)#任务异步出队，Queue内部实现了同步机制
                do(filepath, station)
                self.work_queue.task_done()#通知系统任务完成
            except:
                break

def do_job2(filepath, station):
    for file in filepath:
        try:
            if file[0] == '/':
                pass
            else:
                file = os.path.expanduser('~') +'/' + file
        except:
            pass
        try:
            if scp.copy_file_to_host(file,station,22,'d5000',True)==True:
                pass
            else:
                queue2.put(file+'-->'+station)
        except:
            queue2.put(file+'-->'+station)

def getqueue(filepath,stations,thread):
    work_manager =  WorkManager2(filepath,stations,thread)
    work_manager.wait_allcomplete()
    return queue2

if __name__=="__main__":
    filepath='/home/d5000/xizang/conf/warn_op.ini'
    stations=['lyydev']
    work_manager =  WorkManager2(filepath,stations,10)
    work_manager.wait_allcomplete()

