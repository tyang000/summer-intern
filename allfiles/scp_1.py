#!/usr/bin/env python
#coding=utf-8

import paramiko
import os
import time
import datetime
import sys

def copy_file_to_host(file_dir,host_name,port,username,if_back_up):
    """向指定主机拷贝文件"""

    #获取privae_key
    usr_home = os.path.expanduser('~')
    pkey=usr_home+'/.ssh/id_rsa'
    key=paramiko.RSAKey.from_private_key_file(pkey)
    
    #建立ssh连接
    ssh_connect=paramiko.SSHClient()
    ssh_connect.load_system_host_keys()
    ssh_connect.connect(host_name,port,username,pkey=key)

    #备份文件
    if if_back_up:
        target_file_dir=file_dir+' '+time.strftime("%Y%m%d",time.localtime(time.time()))
        back_up_cmd='mv '+file_dir+' '+target_file_dir
        #print back_up_cmd
        stdin,stdout,stderr=ssh_connect.exec_command(back_up_cmd)
        
        #print stderr.readlines()

    #拷贝文件
    file_path=file_dir.split('/')
    target_path=''
    for index in range(len(file_path)-1):
        target_path+=file_path[index]

    #print target_path
    scp_cmd='scp '+usr_home+'/'+file_dir+' '+host_name+':'+'~/'+target_path
    os.popen(scp_cmd)
    #print scp_cmd

    #检查一致性
    md5_cmd='md5sum '+usr_home+'/'+file_dir
    local_md5=os.popen(md5_cmd).readline().split(' ')[0]
    #print local_md5 

    remote_md5_cmd='md5sum '+'~/'+file_dir
    #print remote_md5_cmd
    stdin,stdout,stderr=ssh_connect.exec_command(remote_md5_cmd)
    remote_md5=stdout.readline().split(' ')[0]
    #print remote_md5

    #关闭连接
    ssh_connect.close()

    #返回拷贝结果
    if local_md5==remote_md5:
        return True
    else:
        return False

if __name__ == "__main__":  
    copy_file_to_host('conf/warn_op.ini','lyydev',22,'d5000',True)
