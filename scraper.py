from bs4 import BeautifulSoup
import requests
import urllib
import re
import config
import sqlite3
import os 
import simplejson
import time
from difflib import get_close_matches


url = "ftp://anonymous:" + config.email + "@ftp.sec.gov/"
sp500 = [x.strip().upper() for x in open('sp500.txt','r')]
  


# urlGen :: Int -> Int -> String
def urlMasterGen(year, quarter, append="index.html"):
  ''' Generate URL to fetch given year and quarter '''
  return url + "edgar/daily-index/" + str(year) + "/QTR" + str(quarter) + "/" + append

def sanitise(filing):
  return [int(filing[0]), filing[2], int(filing[3]), filing[4]]


# getFiling :: Int -> Int -> FilingList
def getFilingList(year, quarter):
  ''' Checks cache for filing, if not then downloads it'''
  directory = 'bin/filings/{0}-{1}.html'.format(year, quarter)
  if not os.path.exists(directory):
    print "Downloading: " + fname
    urllib.urlretrieve(urlMasterGen(year, quarter), directory)
  return open(directory, 'r')

# getFilingDate :: Int -> Filing
def getFilingDate(year, quarter, date):
  '''Gets raw list of filings on a given date string'''
  fname = 'bin/filings/{0}/QTR{1}/{2}'.format(year, quarter, date)
  directory = os.path.dirname(fname)
  if not os.path.exists(directory):
    os.makedirs(directory)
  if not os.path.exists(fname):
    print "Downloading: " + fname
    urllib.urlretrieve(urlMasterGen(year, quarter, date), fname)
  return open(fname, 'r')
    

#pullRecords :: ()
def pullRecords(year, quarter):
  ''' Download all data from specified year and quarter '''
  def progress():
    ''' Prints progress of pass'''
    print '\n'*100
    print message
    ct = int(time.time()-t)
    print '{0} / {1} -- {5} / {6} --- {4}:{2}:{3}'.format(i,n, (ct / 60) % 60, (ct / 1) % 60, ct / 3600, masteri, mastern)
   
  message  = "Processing " + str(year) + " QTR " + str(quarter)
  # fields :: [Int, String, Int]
  fields = ["CIK", "Form Type", "Date Filed"]

  # Get list of filings per day in specific year and quarter
  r = getFilingList(year, quarter)
  soup = BeautifulSoup(r.read())
  urls = [link.get("href") for link in soup(href=re.compile("^master"))]
  mastern = len(urls)
  for (masteri, masterurl) in enumerate(urls):
    # Get list of filings on each specific day
    r = getFilingDate(year, quarter,masterurl)
    data = r.readlines()[10:]  # Remove crap at the top of the file
    filings = [x.split('|') for x in  data]
    n = len(filings)
    for (i, filing) in enumerate([x for x in filings if len(x) == 5 and get_close_matches(x[1], sp500, 1, 0.8)  and x[2] in ["10-K", "10-Q"]]):
      progress()
      directory = 'bin/raw/' + str(filing[0])
      if not os.path.exists(directory):
        os.makedirs(directory)
      extension = os.path.splitext(filing[-1])[-1].strip()
      saveLocation = os.path.join(directory, filing[2] + '-' + str(filing[3]) + extension)
      cursor.execute('''INSERT OR IGNORE INTO companies (CIK, name) VALUES (?, ?)''', filing[:2])
      cursor.execute('''INSERT OR IGNORE INTO filings (CIK, type, date, location) VALUES (?,?,?,?)''', sanitise(filing))
      db.commit()
      if not os.path.isfile(saveLocation): 
        try:
          urllib.urlretrieve(url + filing[-1], saveLocation)
        except IOError:
          with open('error.log', 'a') as fout:
            fout.write(url+filing[-1]) 
      break 
    break  

if __name__ == "__main__":
  db = sqlite3.connect('db/group-practical.dat')
  cursor = db.cursor()
  cursor.execute('''CREATE TABLE IF NOT EXISTS companies
                     ( CIK integer
                     , name text
                     , PRIMARY KEY (CIK))''')
  cursor.execute('''CREATE TABLE IF NOT EXISTS filings
                      ( CIK integer 
                      , type text
                      , date integer
                      , location text
                      , PRIMARY KEY (CIK, date)
                      , FOREIGN KEY(CIK) REFERENCES companies(CIK))''')


                        
                          
  



  years = range(1994, 2009)
  quarters = range(1,5)
  t = time.time()
  for year, quarter in [(y, q) for y in years for q in quarters]:
    if year == 1994 and quarter <= 2: continue  
    try:
      pullRecords(year, quarter)
    except IOError: #Hitting the rate limit
     for i in xrange(60):
        print '\n'*100
        print "FTP Error: Sleeping {0} / 60".format(i+1)
        time.sleep(1)
     pullRecords(year, quarter)





