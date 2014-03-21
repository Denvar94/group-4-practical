# Detect pattern: field label, space, number...

import string

################################################################################
# CONSTANTS
################################################################################

# Characters associated with a data value
dataChars = string.digits + "()$£-%"

# Strings that might seperate columns
colSepStrings = ("   ", "\t", "---", "|")

# The maximum number of characters a column title is likely to occupy
MAX_COL_TITLE_WIDTH = 20

# The maximum expected number of rows a table is expected to have
MAX_TABLE_HEIGHT = 100


################################################################################
# FIELDS
################################################################################

class Field(object):
    def __init__(self, label, alts):
        self.label = label
        self.alts = alts + (label,)

Profit = Field("Profit", ("Total Profit", "Net Profit", "Profits",
                          "Profit (loss)"))
Revenue = Field("Revenue", ("Total Revenue", "Sales", "Total Sales"))
SharePrice = Field("Share Price", ())
Assets = Field("Assets", ("Total Assets", "Combined Assests"))
SharePerDiv = Field("Share Per Dividend", ())
OpMargin = Field("Operating Margin", ())
CashFlow = Field("Cash Flow", ())

Unknown = Field("Not a Field",())
            
fields = (Profit, Revenue, SharePrice, Assets, SharePerDiv,
          OpMargin, CashFlow, Unknown)

#Get the text string to the left of pos, in the same line as pos
def getFieldLabel(line, pos):
    sepStrings = colSepStrings
    for char in dataChars:
        sepString += (char,)
    text = ""
    for i in range(pos - 1, -1, -1):
        for string in sepStrings:
            if string in text:
                return text
        text = line[i] + text
    return text

# Tries to match a given text string with a field
def getField(string):
    for f in field:
        for altStr in f.alts:
            if string in altStr or altStr in string:
                return f
    return Unknown


################################################################################
# TIME PERIODS
################################################################################

class Period(object):
    def __init__(self, year, quarter):
        self.year = year
        self.quarter = quarter
        self.unknown = (year == 0)

Q1 = ("Jan", "Mar", "Q1", "Quarter 1", "1st Quarter", "January", "March")
Q2 = ("Apr", "Jun", "Q2", "Quarter 2", "2nd Quarter", "April", "June")
Q3 = ("Jul", "Sep", "Q3", "Quarter 3", "3rd Quarter", "July", "September")
Q4 = ("Oct", "Dec", "Q4", "Quarter 4", "4th Quarter", "October", "December")

Quarters = (Q1, Q2, Q3, Q4)

# Tries to match a given text string with a time period
def findPeriod(string):
    found = false
    for year in range(1994, 2010):
        if year in string:
            found = true
            break
    if not found:
        year = 0

    found = false
    for quarter in range(1, 5):
        for txt in Quarters[quarter-1]:
            if txt in string:
                found = true
                break
    if not found:
        quarter = 0

    return Period(year, quarter)

        
################################################################################
# FORMATTING
################################################################################

# Returns the column that pos occurs in a given line of text
def getIndent(line, pos):
    indent = 0
    for i in range(0, pos):
        if line[i] == "\t":
            indent += 8 - (indent % 8)
        else:
            indent += 1

# Convert all tab characters in text into the equivalent number of spaces
def flattenTabs(text):
    newText = ""
    for i in range(0, len(text)):
        if text[i] == "\t":
            newText += " " * (8 - (i % 8))
        else:
            newText += text[i]

    
################################################################################
# SCALES
################################################################################

class Scale(object):
    def __init__(self, label, alts, amount):
        self.label = label
        self.alts = alts + (label,)
        self.amount = amount

Thousand = Scale("Thousands", ("1000", "10^3"), 1000)
Million = Scale("Millions", ("1000000", "10^6"), 1000000)
Unit = Scale("Unit", (), 1)

Scales = (Million, Thousand)

# Find a scale that refers to data in a specific line within a list of lines
def findScale(lines, line):     #'line' is a numerical value 
    above = line
    below = line
    while(above >= 0 or below < len(lines)):
        for s in Scales:
            for alt in s.alts:
                if alt in lines(above) or alt in lines(below):
                    return s
        above = max(0, above - 1)
        below = min(len(lines) - 1, below + 1)
    return Unit


################################################################################
# MAIN
################################################################################

# Find the next occurence of a possible data value within a line of text
def getNextDataValRange(line):
    foundNum = false 
    for i in range(0, len(line)):
        if line[i] in string.digits:
            foundNum = true
            start = i
            end = i
            break
    if not foundNum:
        return -1, -1
    else:
        foundEnd = false
        for i in range(end + 1, len(line)):
            if not line[i] in dataChars:
                end = i - 1
                foundEnd = true
                break
        if not foundEnd:
            end = len(line) - 1
        foundStart = false
        for i in range(start - 1, -1, -1):
            if "  " in line[i: end+1] or not line[i] in (dataChars + " "):
                foundStart = true
                start = i+1
                break
        if not foundStart:
            start = 0
    return start, end
# Returns start and end such that the data value is the substring:
# line[start...end + 1)
# If none is found, -1, -1 is returned.

# Extract a numerical value within a data value string
def extractNum(data):
    numString = ""
    for i in range(0, len(data)):
        if data[i] in string.digits:
            numString += data[i]
    return float(numString)

# In a given line, extract a text most likely to be a column header whose
# central character is indented by a specified amount
# It is assumed that the column headers we are interested in are time periods
def searchForHeader(line, indent):
    text = flattenTabs(line)
    for i in range(1, MAX_COL_TITLE_WIDTH // 2):
        left = max(0, indent - i)
        right = min(indent + i, len(line) - 1)
        currStr = text[left: right+1]
        finish = false
        for string in colSepStrings:
            if string in currStr:
                finish = true
        if finish:
            return curStr
        else:
            per = findPeriod(currStr)
            if not per.unknown:
                return curStr
    return ""
            
def main():
    listingsFile = open("FilePaths.txt", "r")
    files = listingsFile.readlines()
    listingsFile.close

    for path in files:
        file = open(path, "r")
        lines = file.readlines()
        file.close()

        for i in range(0, len(lines)):
            line = lines[i]
            pos = 0
            while(pos < len(line)):
                text = line[pos:]
                start, end = getNextDataValRange(text)
                if start == -1:
                    break

                dataLabel = getFieldLabel(line, pos)
                dataField = getField(dataLabel)
                if dataField == Unknown:
                    pos = end + 1
                    continue

                timePrd = findPeriod(dataLabel)
                if timePrd.unknown:
                    for j in range(i, max(-1, i - MAX_TABLE_HEIGHT - 1), -1):
                        colTitle = searchForHeader(j, (start + end) // 2)
                        if not colTitle == "":
                            timePrd = findPeriod(colTitle)
                            break

                if timePrd.unknown:
                    pos = end + 1
                    continue
                else:
                    val = extractNum(line[start : end+1])
                    val *= findScale(i, lines).amount

                    #Do Proper Output Here
                    print(dataField.label + " = " + val)
                    ###
                    break




################################################################################
# OLD CODE
################################################################################

# Assume text[pos,...pos+k) is a number for some k
# Return p <= pos s.t. text[p,..pos+k) is a data value
# (a data value is a number with possible ()$%£- characters
def getNumberRange(text, pos):
    for i in range(pos, -1, -1):
        if not text[i] in dataChars:
            break
    return (i+1)



