#!/usr/bin/env python

from difflib import *
import webbrowser

local_file = open('warn_op.ini','r')
a=local_file.readlines()
#for i in range(len(a)):
#    a[i]=a[i].decode("GB2312",'ignore')

remote_file = open('warn_op2.ini','r')
b=remote_file.readlines()
#for m in range(len(b)):
#    b[m]=b[m].decode("GB2312",'ignore')
   
result_lines = HtmlDiff.make_file(HtmlDiff(),a,b)#.encode('utf-8')
print result_lines
result_file = open('diff_result.html','wb')

result_file.write(result_lines)
webbrowser.open('F:\Python27\wxpython\deff_result.html')
local_file.close()
remote_file.close()
result_file.close()
