#!/usr/bin/env python
#-*- coding:utf-8 -*- 
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

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


def getwork1(IpList,thread=2):
    queue=tool_check.getqueue(IpList,thread)
    return queue

def getwork2(filepath, stations, thread=2):
    queue=tool_deliver.getqueue(filepath,stations,thread)
    return queue


def readconfig():
    #read info from config.ini
    conf=ConfigParser.ConfigParser()
    conf.read('config.ini')
    sections=conf.sections()
    for section in sections:
        option = conf.options(section)
        print section,':',option

def delivertosection(section,filepath):
    #deliver selected file to certain sections
    conf=ConfigParser.ConfigParser()
    conf.read('config.ini')
    options1=conf.options(section)
    alertstring=''
    dictionary=md5.matchdict()
    localhost=dictionary[md5.localip()]
    if localhost in options1:
        options1.remove(localhost)
    else:
        pass
    queue=getwork2(filepath,options1,10)
    if queue.qsize() == 0:
        print "全部工作站已成功复制指定文件！".decode('utf-8','ignore')
    else:
        while queue.qsize() >0: 
            alertstring += queue.get()+' '
        print "以下工作站未成功复制指定文件，请重试或检查！\n".decode('utf-8','ignore')+alertstring
      
def deliverfile(host, filepath):
    #bind to FileList on Page1
    if scp.copy_file_to_host(filepath,host,22,'d5000',True):
        print '复制成功!'.decode('utf-8','ignore')    
    else:
        print '未成功复制，请检查。'.decode('utf-8','ignore')

def comparefile(host,filepath):
    #bind to select submenu on Page1
    scp_cmd = 'scp '+host+":"+filepath+' '+filepath+'_2'
    os.popen(scp_cmd)
    comparetext=os.popen("diff -y "+filepath+' '+filepath+'_2').read()
    os.popen('rm '+filepath+'_2')
    print comparetext
    
def startcheck():
    #start check and print problem file and hosts
    finallist=[]
    IpList=md5.getstation()
    dictionary =md5.matchdict()
    K=md5.getfile()
    stdL=md5.md5sum(md5.localip())
    a=(IpList,dictionary,K,stdL)
    queue=getwork1(a,10)
    while queue.qsize()>0:
        finallist.append(queue.get())   
    for host in finallist:
        if host[2] == []:
            print host[0],' 一切正常'.decode('utf-8','ignore')
        else:
            print host[0],' 不匹配文件如下：\n'.decode('utf-8','ignore'),host[2]

def main():
    while True:   
        print '**************************************************'
        print '欢迎使用本检查与分发工具！'.decode('utf-8','ignore')
        print '1.检查工具'.decode('utf-8','ignore')
        print '2.分发工具'.decode('utf-8','ignore')
        print '9.退出'.decode('utf-8','ignore')
        print '请输入1或2选择一项工具:'.decode('utf-8','ignore')
        uc = input()
        if uc == 9:
            break
        elif uc == 1:
            print '------------------------------------------------------'
            print startcheck()
            print '------------------------------------------------------'
            while True:
                try:
                    print '1.比对文件'.decode('utf-8','ignore')
                    print '2.分发文件'.decode('utf-8','ignore')
                    print '9.返回上级'.decode('utf-8','ignore')
                    print '请选择比对或分发文件：'.decode('utf-8')
                    uc_check = input()
                    if uc_check == 9:
                        break
                    print '请输入工作站名(请加引号)：'.decode('utf-8')
                    host = input ()
                    print '请输入文件的路径(请加引号)：'.decode('utf-8')
                    filepath = input()
                    if filepath[0] == '/':
                        pass
                    else:
                        filepath = os.path.expanduser('~') +'/' + filepath
                    if uc_check == 1:
                        comparefile(host,filepath)
                    elif uc_check == 2:
                        deliverfile(host,filepath)
                    else:
                        print '输入无效，请输入1或2选择一项工具'.decode('utf-8','ignore')
                except:
                    print '请确认工作站和文件路径输入正确并重试。'.decode('utf-8','ignore')
        elif uc == 2:
            print '------------------------------------------------------'
            print readconfig()
            print '------------------------------------------------------'
            while True:
                try:
                    print '1.分发文件'.decode('utf-8','ignore')
                    print '9.返回上级'.decode('utf-8','ignore')
                    print '请选择分发文件或返回上级：'.decode('utf-8')
                    uc_deliver = input()
                    if uc_deliver == 9:
                        break
                    print '请输入工作组名(请加引号)：'.decode('utf-8')
                    section = input ()
                    print '请输入文件的路径(请加引号)：'.decode('utf-8')
                    filepath = input()        
                    if filepath[0] == '/':
                        pass
                    else:
                        filepath = os.path.expanduser('~') +'/' + filepath
                    if uc_deliver == 1:
                        delivertosection(section,filepath)
                    else:
                        print '输入无效，请输入1或9进行选择'.decode('utf-8','ignore')
                except:
                    print '请确认工作组和文件路径输入正确并重试。'.decode('utf-8','ignore')
                
        else:
            print '输入无效，请输入1或2选择一项工具'.decode('utf-8','ignore')
    print '再见。'.decode('utf-8','ignore')

if __name__ == '__main__':
    main()
    
