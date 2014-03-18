from collections import OrderedDict

with open('sp500_all94.txt') as fin:
    lines = (line.rstrip() for line in fin)
    unique_lines = OrderedDict.fromkeys( (line for line in lines if line) )
for line in unique_lines:
    print line
#print unique_lines.keys()