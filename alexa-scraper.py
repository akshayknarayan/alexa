#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import csv

alexa = 'http://www.alexa.com/topsites/global;{}'
base = 'http://www.alexa.com'

def getPageInfo(aTag):
    siteInfoUrl = base + aTag['href']
    siteName = aTag.text
    print siteName
    page = requests.get(siteInfoUrl)
    parsed = BeautifulSoup(page.text)
    link = parsed.select('.offsite_overview')[0]['href']
    return siteName, link

def getSites():
    sites = {}
    for i in xrange(20):
        page = requests.get(alexa.format(i))
        parsed = BeautifulSoup(page.text)
        entries = parsed.select('.desc-container')
        for e in entries:
            name, link = getPageInfo(e.find('a'))
            sites[name] = link
    return sites

if __name__ == '__main__':
    sites = getSites()
    for siteName in sites:
        print siteName, sites[siteName]
    with open('top500.csv', 'w') as f:
        writer = csv.writer(f)
        for siteName in sites:
            writer.writerow([siteName, sites[siteName]])
