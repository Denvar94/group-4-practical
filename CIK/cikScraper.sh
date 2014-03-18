#!/bin/bash
# Basic algorithm idea
# 1 - for each year get a list of companies that were in the SP500 THAT YEAR
# 2 - COMPILE A LIST, WITHOUT DUPLICATES

# 3 - RUN THROUGH THE LIST OF ALL COMPANIES FROM 94 -2009 
# 4 - GRAB the CIK's for the relevant companies

#-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-
# run through all companies
while read symbol; do

#stage 4 Grab CIK for symbol:
#make it upper case
symb=$(echo $symbol|tr '[:lower:]' '[:upper:]')

#grep for the company
firstGrepResult=`grep "$symb" *|head -1`

#grep should return the LINE from companies.idx (includes CIK number)
#this line takes the CIK number from the grep output
CIK=`echo $firstGrepResult|rev|cut -d " " -f3|rev`

#output separated by a comma
echo $symb,$CIK
done < "sp500_94_noDuplicates.txt"

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#LEFTOVER CODE FROM EARLIER ATTEMPTS, BUT I'VE LEFT IT IN AS SOME OF IT
#MAY BE USEFUL LATER.

# grep '^Subject:' read-messages | cut -c10-80
# sed -n 16224,16482p filename > newfile

