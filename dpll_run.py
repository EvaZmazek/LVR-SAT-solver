import copy
from boolean import *
from dpll_algoritem import *
import sys

print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: " , str(sys.argv))

file1 = open(sys.argv[1], 'r')
file2 = open(sys.argv[2], 'r')

for line in file1:
    print(line)
