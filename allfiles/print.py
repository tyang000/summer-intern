import sys
f=open('output.txt','w')

a='asdf'
b='asdf'
print >>f,"asasdfawecfbsgb",a,b
print >>f,"asdfawefgr",a
print >>f,"avfgdgdfgdddddddddd",b




f=open('output.txt')
x=f.readlines()
finalstring = ''
for string in x:
    finalstring += string
print finalstring
