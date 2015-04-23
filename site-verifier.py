#!/usr/bin/python

import sys
import csv
import requests

userAgentHeader = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17'}

def checkResponse(r, url):
    if (r.status_code != 200):
        if (r.status_code == 301 or r.status_code == 302):
            redirect = r.headers['location']
            if (redirect.startswith('https://')):
                return 'https', redirect
            elif (redirect.startswith('http://')):
                return verifySite(name, redirect)
            else:
                print 'ambiguous:', r.headers, r.status_code, r.text
                return None, url

        elif (r.status_code == 405):
            g = requests.get(url, headers=userAgentHeader)
            return checkResponse(g, url)

        elif (r.status_code == 403):
            r = requests.head(url, headers=userAgentHeader)
            return checkResponse(r, url)

        elif (r.status_code == 404):
            return '404', url
    else:
        g = requests.get(url)
        if (g.status_code == 200):
            return 'http', url

def verifySite(name, url):
    try:
        r = requests.head(url)
        return checkResponse(r, url)
    except requests.exceptions.ConnectionError:
        print url, 'connection error'

sites = {}

if (len(sys.argv) < 2):
    print 'Usage: python site-verifier.py <csv-file>'
    sys.exit(0)
else:
    with open(sys.argv[1]) as f:
        reader = csv.reader(f)
        for name, url in reader:
            check, url = verifySite(name, url)
            if check in sites:
                sites[check].append((name, url))
            else:
                sites[check] = [(name, url)]
            print name, url, check

    print '404 sites:', len(sites['404'])
    print 'http sites:', len(sites['http'])
    print 'https sites:', len(sites['https'])
    print 'both sites:', len(sites['both'])
