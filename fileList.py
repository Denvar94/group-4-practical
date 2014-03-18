from collections import OrderedDict

with open('2sp500.txt') as fin:
    lines = (line.rstrip() for line in fin)
    unique_lines = OrderedDict.fromkeys( (line for line in lines if line) )

print unique_lines.keys()