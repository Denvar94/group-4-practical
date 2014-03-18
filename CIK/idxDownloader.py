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
  

