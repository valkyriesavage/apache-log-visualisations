#!/usr/bin/python

import os
import re
import sqlite3
import subprocess
import sys
import time
from urllib2 import unquote

IP_REGEX = re.compile(r'(\d{1,3}.){4}')
SEARCH_REGEX = re.compile(r'(p|p1)=(?P<search>.*?)(&|\s)')
LIVE_LOG_TO_READ = "/opt/viz/log.bigsample"
PID_FILE = "/tmp/logtailer.pid"
SQLITE_LIVE_FILE = "/tmp/logtailer"

def already_running():
    try:
        f = open(PID_FILE)
        pid = int(f.readline())
        f.close()
        print 'this appears to already be running...'
        return True
    except (IOError, ValueError):
        f = open(PID_FILE, 'w')
        f.write(str(os.getpid()))
        f.close()
        return False

def clean_up():
    retcode = subprocess.call(['rm', PID_FILE])

def follow(log):
    log.seek(0,2)
    while True:
        line = log.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def get_search_from_line(line):
    if SEARCH_REGEX.search(line):
        return SEARCH_REGEX.search(line).group('search')
    return ''

def prettify_search(search):
    search = search.lower()
    search = search.replace('+', ' ')
    search = unquote(search)
    return search

if __name__ == '__main__':
    if already_running():
        sys.exit(0)
    print 'not yet running... here we go!'

    live_conn = sqlite3.connect(SQLITE_LIVE_FILE)
    live_db = live_conn.cursor()
    live_db.execute("""
            create table if not exists ip_search
            (rowid INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT,
             search TEXT, timestamp DEFAULT CURRENT_TIMESTAMP);
            """)
    live_log = open(LIVE_LOG_TO_READ, 'r')
    loglines = follow(live_log)
    for line in loglines:
        if not "GET /search?" in line:
            continue
        ip = line.split(' - ')[0]
        if not IP_REGEX.match(ip):
            continue
        search = prettify_search(get_search_from_line(line))

        live_db.execute("insert into ip_search (ip, search) values ('%s', '%s')" %\
                    (ip, search.replace("'", '%%QUOTE%%')))
        live_conn.commit()
