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
        print "������û��Ȩ�޷ַ��ļ�������Ҫ����Ȩ������authorization.ini����ӣ�".decode('GB2312','ignore')
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
            print filepath[i2]+ ':  �ļ������пո����޸ĺ�����'.decode('GB2312','ignore')
        elif os.popen('ls -lh '+filepath[i2].encode('GBK')).read()[0].split()[0] == 'l':
            print filepath[i2]+ ':  ��link�ļ������ַܷ�'.decode('GB2312','ignore')
        else:
            finalfilepath.append(filepath[i2])
    queue=getwork2(finalfilepath,options,10)
    if queue.qsize() == 0:
        print "ȫ������վ�ѳɹ�����ָ���ļ���".decode("GB2312",'ignore')
    else:
        while queue.qsize() >0: 
            alertstring += queue.get()+'\n'
        print "���¹���վδ�ɹ�����ָ���ļ��������Ի��飡\n".decode("GB2312",'ignore')+alertstring
      
def deliverfile(host, filepath):

    if scp.copy_file_to_host(filepath,host,22,'d5000',True):
        print '���Ƴɹ�!'.decode("GB2312",'ignore')    
    else:
        print 'δ�ɹ����ƣ����顣'.decode("GB2312",'ignore')

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
                f.write(host[0]+' һ������\n'.decode("GB2312",'ignore'))
                print host[0],' һ������'.decode("GB2312",'ignore')
            else:
                f.write(host[0]+'\n')
                print host[0]        
        else:
            f.write(host[0]+' ��ƥ���ļ����£�\n'.decode("GB2312",'ignore'))
            print host[0],' ��ƥ���ļ����£�\n'.decode("GB2312",'ignore')
            for info in host[2]:
                f.write(info+'\n')
                print info
    f.close()
def main():
    while True:   
        print '**************************************************'
        print '��ӭʹ�ñ������ַ����ߣ�'.decode("GB2312",'ignore')
        print '1.��鹤��'.decode("GB2312",'ignore')
        print '2.�ַ�����'.decode("GB2312",'ignore')
        print '9.�˳�'.decode("GB2312",'ignore')
        print '������1��2ѡ��һ���:'.decode("GB2312",'ignore')
        uc = input()
        if uc == 9:
            break
        elif uc == 1:
            print '------------------------------------------------------'
            print startcheck()
            print '------------------------------------------------------'
            while True:
                try:
                    print '1.�ȶ��ļ�'.decode("GB2312",'ignore')
                    print '2.�ַ��ļ�'.decode("GB2312",'ignore')
                    print '9.�����ϼ�'.decode("GB2312",'ignore')
                    print '��ѡ��ȶԻ�ַ��ļ���'.decode("GB2312")
                    uc_check = input()
                    if uc_check == 9:
                        break
                    print '�����빤��վ����'.decode("GB2312")
                    host = raw_input ()
                    print '�������ļ���·����'.decode("GB2312")
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
                        print '������Ч��������1��2ѡ��һ���'.decode("GB2312",'ignore')
                except:
                    print '��ȷ�Ϲ���վ���ļ�·��������ȷ�����ԡ�'.decode("GB2312",'ignore')
        elif uc == 2:
            print '------------------------------------------------------'
            print readconfig()
            print '------------------------------------------------------'
            while True:
                try:
                    print '1.�ַ��ļ�(�ɶ�ѡ)'.decode("GB2312",'ignore')
                    print '9.�����ϼ�'.decode("GB2312",'ignore')
                    print '��ѡ��ַ��ļ��򷵻��ϼ���'.decode("GB2312")
                    uc_deliver = input()
                    if uc_deliver == 9:
                        break
                    print '�����빤��������'.decode("GB2312")
                    section = raw_input ()
                    print '�������ļ���·�����Էֺŷָ�ͽ�β����'.decode("GB2312")
                    filepath = raw_input()        
                    if uc_deliver == 1:
                        delivertosection(section,filepath)
                    else:
                        print '������Ч��������1��9����ѡ��'.decode("GB2312",'ignore')
                except:
                    print '��ȷ�Ϲ�������ļ�·��������ȷ�����ԡ�'.decode("GB2312",'ignore')
                
        else:
            print '������Ч��������1��2ѡ��һ���'.decode("GB2312",'ignore')
    print '�ټ���'.decode("GB2312",'ignore')

if __name__ == '__main__':
    main()
    
