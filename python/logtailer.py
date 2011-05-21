#!/usr/bin/python

import re
import sqlite3
import time
from urllib2 import unquote

IP_REGEX = re.compile(r'(\d{1,3}.){4}')
SEARCH_REGEX = re.compile(r'(p|p1)=(?P<search>.*?)(&|\s)')
LOG_TO_READ = "/home/valkyrie/projects/inspire-log-viz/log.bigsample"

def follow(log):
    # for live tailing, uncomment me!
    #log.seek(0,2)
    while True:
        line = log.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def get_search_from_line(line):
    return SEARCH_REGEX.search(line).group('search')

def prettify_search(search):
    search = search.lower()
    search = search.replace('+', ' ')
    search = unquote(search)
    return search

if __name__ == '__main__':
    conn = sqlite3.connect('/tmp/logtailer')
    db = conn.cursor()
    db.execute("create table if not exists ip_search (ip, search);")
    log = open(LOG_TO_READ, 'r')
    loglines = follow(log)
    for line in loglines:
        if not "GET /search?" in line:
            continue
        ip = line.split(' - ')[0]
        if not IP_REGEX.match(ip):
            continue
        search = prettify_search(get_search_from_line(line))

        db.execute("insert into ip_search values ('%s', '%s')" %\
                    (ip, search))
        conn.commit()
