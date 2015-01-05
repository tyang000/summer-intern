import difflib
from difflib import *

a = 'pythonclub.org is wonderful'
b = 'Pythonclub.org also wonderful'
s = difflib.SequenceMatcher(None, a, b)
print s
