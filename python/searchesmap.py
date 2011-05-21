#!/usr/bin/python

import cgi
import json
from pygeoip import GeoIP
import sqlite3

GI = GeoIP("/home/valkyrie/projects/inspire-log-viz/src/GeoLiteCity.dat")

def get_lat_long_pair(ip):
    record = GI.record_by_addr(ip)
    if not record:
        return (0,0)
    return (record['latitude'], record['longitude'])

def pull_search_from_db(mapped):
    mapped = int(mapped) + 1; # dumbass
    conn = sqlite3.connect("/tmp/logtailer")
    db = conn.cursor()
    db.execute("select * from ip_search where rowid="+str(mapped))
    for row in db:
        ip, search = row
        search = search.replace('%%QUOTE%%', "'")
        return ip, search

print "Content-type: application/json"
print

fs = cgi.FieldStorage()
if fs.has_key('mapped'):
    ip, search = pull_search_from_db(fs.getvalue('mapped'))

    json_obj = []
    latitude, longitude = get_lat_long_pair(ip)
    json_obj = {
                "latitude": latitude,
                "longitude" : longitude,
                "search" : search
                }

    print json.dumps(json_obj)
