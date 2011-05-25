#!/usr/bin/python

import cgi
import json
from pygeoip import GeoIP
import sqlite3

GI = GeoIP("/opt/viz/thirdparty/GeoLiteCity.dat")
LIVE_DB = '/tmp/logtailer'
REPLAY_DB = '/tmp/oldlog'

def get_lat_long_pair(ip):
    record = GI.record_by_addr(ip)
    if not record:
        return (0,0)
    return (record['latitude'], record['longitude'])

def pull_search_from_db(mapped, live):
    if live:
        log = LIVE_DB
    else:
        log = REPLAY_DB
    conn = sqlite3.connect(log)
    db = conn.cursor()

    row_total_query = "select count(*) from ip_search;"
    db.execute(row_total_query)
    row_total = db.fetchone()[0]

    if mapped > 0:
        query = "select * from ip_search where rowid=%d;" % mapped
    elif live:
        query = "select * from ip_search where timestamp>datetime('now','-5 minutes');"
    else:
        query = "select * from ip_search where rowid=1;"
    db.execute(query)
    row = db.fetchone()
    row_id, ip, search, timestamp = row
    search = search.replace('%%QUOTE%%', "'")

    return row_total, row_id, ip, search, timestamp

print "Content-type: application/json"
print

fs = cgi.FieldStorage()

live = True

if fs.has_key('live'):
    live = (fs.getvalue('live') == 'true')

if fs.has_key('mapped'):
    rows, row_id, ip, search, timestamp = pull_search_from_db(int(fs.getvalue('mapped')), live=live)
else:
    rows, row_id, ip, search, timestamp = pull_search_from_db(mapped=-1, live=live)

latitude, longitude = get_lat_long_pair(ip)
json_obj = [rows, {
            "latitude": latitude,
            "longitude" : longitude,
            "search" : search,
            "timestamp" : timestamp,
            "id" : row_id,
            }]
print json.dumps(json_obj)
