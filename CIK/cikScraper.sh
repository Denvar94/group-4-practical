#!/bin/bash
#1for each year get a list of companies that were in the SP500 THAT YEAR
#2COMPILE A LIST, WITHOUT DUPLICATES

#3 RUN THROUGH THE LIST OF ALL COMPANIES FROM 94 -2009 
#4 GRAB the CIK's for the relevant companies

#3 run through all companies
symbol="AES Corp"
while read symbol; do

#4 Grab CIK for symbol
#echo $symbol
symb=$(echo $symbol|tr '[:lower:]' '[:upper:]')
#echo $symb

firstGrepResult=`grep "$symb" *|head -1`
CIK=`echo $firstGrepResult|rev|cut -d " " -f3|rev`

echo $symb,$CIK
done < "sp500_historical_to2000.txt"

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#1for x <- (all the input file names)
#2find  COMPANY CONFORMED NAME:			x central Index key
#3    then from that file take the line with x and the line after 
#4		CENTRAL INDEX KEY:			0000062765
#5		and return the last word of those two lines


#1
# while read symbol ; do 
# #  stock $symbol
# 
# # 2. 
# echo $symbol
# symbol="${symbol^^}"
# 
# 
# echo "grep -A2 \"COMPANY CONFORMED NAME:\s*$symbol\" ../Group\ 4\ DATA/bin/raw/ -r -m 2"
# a=$(grep -A2 "COMPANY CONFORMED NAME:\s*$symbol" ../Group\ 4\ DATA/bin/raw/ -r -m 2)
# #a=$(grep -r -m 1 -A 2 $symbol ../Group\ 4\ DATA/)
# 
# echo $a 
# 
# #2/3 grep '^Subject:' read-messages 
# #3 cut -c10-80
# 
# #3 sed -n 16224,16482p filename > newfile
# 
# done < 2sp500.txt
# 
# 
# 
# 		
# 		