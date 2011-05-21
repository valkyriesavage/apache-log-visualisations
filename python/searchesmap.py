#!/usr/bin/python

import cgi
import json
import os
from pygeoip import GeoIP
import re
import sqlite3
import sys

GI = GeoIP("/home/valkyrie/projects/inspire-log-viz/src/GeoLiteCity.dat")
LOG_TO_READ = "/home/valkyrie/projects/inspire-log-viz/log.sample"
IP_REGEX = re.compile(r'(\d{1,3}.){4}')
SEARCH_REGEX = re.compile(r'(p|p1)=(?P<search>.*?)(&|\s)')

# URL DECODE from http://jaytaylor.com/blog/2010/04/25/urldecode-for-python-one-liner/
_UD = re.compile('%([0-9a-hA-H]{2})', re.MULTILINE)
URLDECODE = lambda x: _UD.sub(lambda m: chr(int(m.group(1), 16)), x)

def get_lat_long_pair(ip):
    record = GI.record_by_addr(ip)
    if not record:
        return (0,0)
    return (record['latitude'], record['longitude'])

def get_search_from_line(line):
    return SEARCH_REGEX.search(line).group('search')

def prettify_search(search):
    search = search.lower()
    search = search.replace('+', ' ')
    search = URLDECODE(search)
    return search

def pull_list_from_db(mapped):
    conn = sqlite3.connect("/tmp/logtailer")
    db = conn.cursor()
    db.execute("select * from ip_search where rowid="+mapped+";")
    for row in db:
        # should only ever be one!
        return row

def pull_list_from_log(mapped):
    log = open(LOG_TO_READ)
    ips_and_searches = []
    for line in log:
        if not "GET /search?" in line:
            continue
        ip = line.split(' - ')[0]
        if not IP_REGEX.match(ip):
            continue
        search = prettify_search(get_search_from_line(line))
        #search = mapped
        ips_and_searches.append((ip, search))
    return ips_and_searches

print "Content-type: application/json"
print

form = cgi.FieldStorage()
if form.has_key('mapped'):
    ips_and_searches = pull_list_from_db(form['mapped'])
else:
    ips_and_searches = pull_list_from_log('')

json_obj = []
for ip, search in ips_and_searches:
    latitude, longitude = get_lat_long_pair(ip)
    json_obj.append({
            "latitude": latitude,
            "longitude" : longitude,
            "search" : search
            })

print json.dumps(json_obj)
