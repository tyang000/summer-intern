#!/usr/bin/env python
#-*- coding:GB2312 -*- 
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

import sys
reload(sys)
sys.setdefaultencoding( "GB2312" )


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
    f=open('authorization.ini').readlines()
    ips=''
    for ip in f:
        ips += ip
    if md5.localip() in ips:
        pass
    else:
        print "该主机没有权限分发文件，如需要赋予权限请在authorization.ini中添加！".decode('GB2312','ignore')
        raise SyntaxError
    conf=ConfigParser.ConfigParser()
    conf.read('config.ini')
    options1=conf.options(section)
    alertstring=''
    options=[]
    dictionary=md5.matchdict2()
    for i in range(len(options1)):
        try:
            if dictionary[options1[i]] == md5.localip():
                pass
            else:
                options.append(options1[i])
        except:
            pass
    finalfilepath=[]
    filepath=filepath.split(';')
    filepath=filepath[:-1]
    for i2 in range(len(filepath)):
        try:
            if filepath[i2][0]=='/':
                pass
            else:
                filepath[i2]=os.path.expanduser('~')+'/'+filepath[i2]
        except:
            pass
        if ' ' in filepath[i2]:
            print filepath[i2]+ ':  文件名中有空格，请修改后重试'.decode('GB2312','ignore')
        elif os.popen('ls -lh '+filepath[i2].encode('GBK')).read()[0].split()[0] == 'l':
            print filepath[i2]+ ':  是link文件，不能分发'.decode('GB2312','ignore')
        else:
            finalfilepath.append(filepath[i2])
    queue=getwork2(finalfilepath,options,10)
    if queue.qsize() == 0:
        print "全部工作站已成功复制指定文件！".decode("GB2312",'ignore')
    else:
        while queue.qsize() >0: 
            alertstring += queue.get()+'\n'
        print "以下工作站未成功复制指定文件，请重试或检查！\n".decode("GB2312",'ignore')+alertstring
      
def deliverfile(host, filepath):

    if scp.copy_file_to_host(filepath,host,22,'d5000',True):
        print '复制成功!'.decode("GB2312",'ignore')    
    else:
        print '未成功复制，请检查。'.decode("GB2312",'ignore')

def comparefile(host,probfile):

    scp_cmd = 'scp '+host+":"+probfile+' '+probfile+'_2'
    os.popen(scp_cmd)
    local_file = open(probfile)
    a=local_file.readlines()
    remote_file = open(probfile+'_2')
    b=remote_file.readlines()

    result_lines = HtmlDiff.make_file(HtmlDiff(),a,b)

    result_file = open('diff_result.html','w')
    result_file.write(result_lines)
    
    webbrowser.open('diff_result.html')
    
    local_file.close()
    remote_file.close()
    result_file.close()
    
    os.popen('rm '+probfile+'_2')
    
def startcheck():
    #start check and print problem file and hosts
    f=open('results.txt','w')
    f.write(time.ctime()+'\n')
    finallist=[]
    IpList=md5.getstation()
    dictionary =md5.matchdict()
    K=md5.getfile()
    print 'checking local files.....'
    stdL=md5.md5sum2(md5.localip())
    a=(IpList,dictionary,K,stdL)
    queue=getwork1(a,10)
    while queue.qsize()>0:
        finallist.append(queue.get())   
    for host in finallist:
        if host[2] == []or host[2]=='':
            if host[0] in dictionary.values():
                f.write(host[0]+' 一切正常\n'.decode("GB2312",'ignore'))
                print host[0],' 一切正常'.decode("GB2312",'ignore')
            else:
                f.write(host[0]+'\n')
                print host[0]        
        else:
            f.write(host[0]+' 不匹配文件如下：\n'.decode("GB2312",'ignore'))
            print host[0],' 不匹配文件如下：\n'.decode("GB2312",'ignore')
            for info in host[2]:
                f.write(info+'\n')
                print info
    f.close()
def main():
    while True:   
        print '**************************************************'
        print '欢迎使用本检查与分发工具！'.decode("GB2312",'ignore')
        print '1.检查工具'.decode("GB2312",'ignore')
        print '2.分发工具'.decode("GB2312",'ignore')
        print '9.退出'.decode("GB2312",'ignore')
        print '请输入1或2选择一项工具:'.decode("GB2312",'ignore')
        uc = input()
        if uc == 9:
            break
        elif uc == 1:
            print '------------------------------------------------------'
            print startcheck()
            print '------------------------------------------------------'
            while True:
                try:
                    print '1.比对文件'.decode("GB2312",'ignore')
                    print '2.分发文件'.decode("GB2312",'ignore')
                    print '9.返回上级'.decode("GB2312",'ignore')
                    print '请选择比对或分发文件：'.decode("GB2312")
                    uc_check = input()
                    if uc_check == 9:
                        break
                    print '请输入工作站名：'.decode("GB2312")
                    host = raw_input ()
                    print '请输入文件的路径：'.decode("GB2312")
                    filepath = raw_input()
                    if filepath[0] == '/':
                        pass
                    else:
                        filepath = os.path.expanduser('~') +'/' + filepath
                    if uc_check == 1:
                        comparefile(host,filepath)
                    elif uc_check == 2:
                        deliverfile(host,filepath)
                    else:
                        print '输入无效，请输入1或2选择一项工具'.decode("GB2312",'ignore')
                except:
                    print '请确认工作站和文件路径输入正确并重试。'.decode("GB2312",'ignore')
        elif uc == 2:
            print '------------------------------------------------------'
            print readconfig()
            print '------------------------------------------------------'
            while True:
                try:
                    print '1.分发文件(可多选)'.decode("GB2312",'ignore')
                    print '9.返回上级'.decode("GB2312",'ignore')
                    print '请选择分发文件或返回上级：'.decode("GB2312")
                    uc_deliver = input()
                    if uc_deliver == 9:
                        break
                    print '请输入工作组名：'.decode("GB2312")
                    section = raw_input ()
                    print '请输入文件的路径（以分号分割和结尾）：'.decode("GB2312")
                    filepath = raw_input()        
                    if uc_deliver == 1:
                        delivertosection(section,filepath)
                    else:
                        print '输入无效，请输入1或9进行选择'.decode("GB2312",'ignore')
                except:
                    print '请确认工作组和文件路径输入正确并重试。'.decode("GB2312",'ignore')
                
        else:
            print '输入无效，请输入1或2选择一项工具'.decode("GB2312",'ignore')
    print '再见。'.decode("GB2312",'ignore')

if __name__ == '__main__':
    main()
    
