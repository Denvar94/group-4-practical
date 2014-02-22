from bs4 import BeautifulSoup
import requests
import urllib
import re
import config
import pymongo
import  os 
import simplejson
import time
from difflib import get_close_matches

client = pymongo.MongoClient()
db = client['group-practical']
filingsDB = db['filings']
companiesDB = db['companies']

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
    urllib.urlretrieve(urlMasterGen(year, quarter, date), fname)
  return open(fname, 'r')
    

#pullRecords :: ()
def pullRecords(year, quarter):
  ''' Download all data from specified year and quarter '''
  def progress():
    print '\n'*100
    print message
    ct = int(time.time()-t)
    print '{0} / {1} -- {5} / {6} --- {4}:{2}:{3}'.format(i,n, (ct / 60) % 60, (ct / 1) % 60, ct / 3600, masteri, mastern)
    
  # fields :: [Int, String, String, Int, String]
  fields = ["CIK", "Form Type", "Date Filed"]
  message  = "Processing " + str(year) + " QTR " + str(quarter)
  print urlMasterGen(year, quarter)
  r = getFilingList(year, quarter)
  soup = BeautifulSoup(r.read())
  urls = [link.get("href") for link in soup(href=re.compile("^master"))]
  mastern = len(urls)
  for (masteri, masterurl) in enumerate(urls):
    r = getFilingDate(year, quarter,masterurl)
    data = r.readlines()[10:]  # Remove crap at the top of the file
    filings = [x.split('|') for x in  data]
    n = len(filings)
    for (i, filing) in enumerate([x for x in filings if len(x) == 5 and get_close_matches(x[1], sp500, 1, 0.8)  and x[2] in ["10-K", "10-Q"]]):
      progress()
      print filing[1]
      print get_close_matches(filing[1], sp500,5,  0.8) 
      directory = 'bin/raw/' + str(filing[0])
      if not os.path.exists(directory):
        os.makedirs(directory)
      extension = os.path.splitext(filing[-1])[-1].strip()
      saveLocation = os.path.join(directory, filing[2] + '-' + str(filing[3]) + extension)
      d =  {"CIK" :int(filing[0]), "Name" : filing[1]}
      companiesDB.insert(d)
      d = dict(zip(fields, sanitise(filing)))
      filingsDB.insert(d)
      if not os.path.isfile(saveLocation): 
        try:
          urllib.urlretrieve(url + filing[-1], saveLocation)
        except IOError:
          with open('error.log', 'a') as fout:
            fout.write(url+filing[-1])
        

#ftp.sec.gov/edgar/data/100441/0000950135-94-000566.txt

if __name__ == "__main__":
  years = range(1994, 2000)
  quarters = range(1,5)
  t = time.time()
  for year, quarter in [(y, q) for y in years for q in quarters]:
    if year == 1994 and quarter <= 2: continue 
    pullRecords(year, quarter)
    #except IOError: #Hitting the rate limit
    # for i in xrange(60):
    #    print '\n'*100
    #    print "FTP Error: Sleeping {0} / 60".format(i+1)
    #    time.sleep(1)
    #  pullRecords(year, quarter)




