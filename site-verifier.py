#!/usr/bin/python

import sys
import csv
import requests

userAgentHeader = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17'}

def get(url, head=None):
    if (not head):
        try:
            r = requests.get(url)
            return r
        except:
            return None
    else:
        try:
            r = requests.get(url, headers=head)
            return r
        except:
            return None

def head(url, head=None):
    if (not head):
        try:
            r = requests.head(url)
            return r
        except:
            return None
    else:
        try:
            r = requests.head(url, headers=head)
            return r
        except:
            return None

def verifySite(r, url, userAgent=False, usedGetRequest=False):
    if (not r):
        if (not userAgent):
            g = get(url, head=userAgentHeader)
            if (g):
                return verifySite(g, url, usedGetRequest=True, userAgent=True)
            else:
                return 'error', url
        else:
            return 'error', url

    if (r.status_code == 200):
        g = get(url)
        if (g and g.status_code == 200):
            https_url = 'https://' + url.split('http://')[-1]
            print 'got http, trying https', https_url
            g = get(https_url)
            if (g and g.status_code == 200):
                return 'both', url
            else:
                return 'http', url
        else:
            return 'http_head', url
    elif (r.status_code == 301 or r.status_code == 302):
        redirect = r.headers['location']
        if (redirect.startswith('https://')):
            return 'https', redirect
        elif (not usedGetRequest):
            g = get(url)
            if (g):
                return verifySite(g, url, usedGetRequest=True)
            else:
                return 'redirect error', url
        elif (not userAgent):
            g = get(redirect, head=userAgentHeader)
            if (g):
                return verifySite(g, redirect, usedGetRequest=True, userAgent=True)
            else:
                return 'redirect error', redirect
        else:
            return 'redirect loop', redirect
    else:
        if (not usedGetRequest):
            g = get(url)
            if (g):
                return verifySite(g, url, usedGetRequest=True)
            else:
                return str(r.status_code), url
        elif (not userAgent):
            g = get(url, head=userAgentHeader)
            if (g):
                return verifySite(g, url, usedGetRequest=True, userAgent=True)
            else:
                return str(r.status_code), url
        else:
            return str(r.status_code), url

sites = {}

if (len(sys.argv) < 2):
    print 'Usage: python site-verifier.py <csv-file>'
    sys.exit(0)
else:
    with open(sys.argv[1]) as f:
        reader = csv.reader(f)
        for name, url in reader:
            r = head(url)
            check, url = verifySite(r, url)
            if check in sites:
                sites[check].append((name, url))
            else:
                sites[check] = [(name, url)]
            print name, url, check

    print 'http sites:', len(sites['http'])
    print 'https sites:', len(sites['https'])
    print 'both sites:', len(sites['both']) if 'both' in sites else '0'

