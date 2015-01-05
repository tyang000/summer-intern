f=open('output.txt')
x=f.readlines()
finalstring = ''
for string in x:
    finalstring += string
print finalstring
