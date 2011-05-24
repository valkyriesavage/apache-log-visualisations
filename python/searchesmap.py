#!/usr/bin/python

import cgi
import json
from pygeoip import GeoIP
import sqlite3

GI = GeoIP("/opt/viz/thirdparty/GeoLiteCity.dat")

def get_lat_long_pair(ip):
    record = GI.record_by_addr(ip)
    if not record:
        return (0,0)
    return (record['latitude'], record['longitude'])

def pull_search_from_db(mapped=-1):
    conn = sqlite3.connect("/tmp/logtailer")
    db = conn.cursor()
    if mapped > 0:
        query = "select * from ip_search where rowid=%d;" % mapped
    else:
        query = "select * from ip_search where timestamp>datetime('now','-5 minutes');"
    db.execute(query)
    for row in db:
        row_id, ip, search, timestamp = row
        search = search.replace('%%QUOTE%%', "'")
        # we can really only return one at a time
        return row_id, ip, search, timestamp

print "Content-type: application/json"
print

fs = cgi.FieldStorage()
if fs.has_key('mapped'):
    row_id, ip, search, timestamp = pull_search_from_db(int(fs.getvalue('mapped')))

else:
    row_id, ip, search, timestamp = pull_search_from_db()

latitude, longitude = get_lat_long_pair(ip)
json_obj = {
            "latitude": latitude,
            "longitude" : longitude,
            "search" : search,
            "timestamp" : timestamp,
            "id" : row_id,
            }
print json.dumps(json_obj)
