import re
import glob
import os

def grep(pattern,fileObj):
  r=[]
  linenumber=0
  for line in fileObj:
    linenumber +=1
    if re.search(pattern,line):
      r.append((linenumber,line))
  return r
  
with open('sp500_historical_to2000.txt') as sp500list:
    for company in iter(sp500list.readline, ''):
    
        rootdir = '.'
        os.chdir(rootdir)
        #print "new company:"
        for file in glob.glob("*.idx"):
            with open(file) as toFind:
                result=grep(company.upper(), toFind);
                #if(result<>[]):
                print company
                print result
       
        





# path to the file to read from
# my_file = "/home/eday/test.txt"
# # what to look in each line
# look_for = "CHECKOUT_REVISION"
# # variable to store lines containing CHECKOUT_REVISION
# temp = []
# 
# with open(my_file, "r") as file_to_read:
#     for line in file_to_read:
#         if look_for in line:
#             temp.append(line)
# print unique_lines.keys()