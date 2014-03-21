
# Getting Started

This repositary only contains the source files. Everyone will need to download the data and generate the fake data for themselves. 

To install all dependencies, you should download [pip](https://pypi.python.org/pypi/pip) and then use the command `pip install -r libraries.pip`.

Virtualenv's are also very useful (short for virtual environment). Read about them here http://simononsoftware.com/virtualenv-tutorial/



# Implementation

There are three distinct parts to the project. Each can be tackled seperately but it is expected that the parser will take up a disproporiate amount of time.

## Parser

The data is initially downloaded using the requests library and then stored in bin/raw/. Setup.py will download this for you if it doesn't exist.

Beautiful Soup is a Python library which makes light work of parsing HTML documents into usable formats. Once the information is downloaded, most of the work will be working out how we can coerce this tree into the infromation we want.

Once we have parsed the data, we can dump the information into some sort of database. Probably either sqlite3 of mongodb.

## API

This step will link together the database and the visualisation. How this is implemented depends a lot on how we decide to do the visualisation.

## Visualisation

It was suggested that we did this in the browser, I think this is a good idea. There are lots of javascript libraries which will allow for as much or as little control we like over the visualisation.

One suggestion was using D3 (http://d3js.org/), not something I have ever done.

There are about a million different ways though (http://www.creativebloq.com/design-tools/data-visualization-712402)

# File list and explanations

"1994-2013 EOY SP500 Snapshots.xlsx" - list of constituents of the SP500 at year end
for years 1994-2014

##CIK subfolder
"removeDuplicates.py" - removes duplicate names from a list. 
So if the list was "a,a,b,c,d" it would output "a,b,c,d". 
Some formatting is required to clean the output.

"sp500_all94" - all constituents back to 94, needs duplicates removed

"sp500_historical_to2000" - all constituents back to 2000

"companies with cik.csv" - an initial (incomplete) list of companies with CIK's

"company...idx" - index files from the SEC matching up company names with CIK's 

"idxDownloader.py" - incomplete scraper to scrape more idx files off of the SEC server

"cikScraper.sh" - given a specified input list of companies, matches up companies to CIK
uses the index files to try and perform matching. is somewhat successful.

"sp500_94_ciks.csv" - is the output of Company names with CIKs but it is only 60% complete.
