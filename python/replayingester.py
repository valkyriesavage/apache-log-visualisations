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
REPLAY_LOG_TO_READ = "/opt/viz/log.oneday"
PID_FILE = "/tmp/logtailer.pid"
SQLITE_REPLAY_FILE = "/tmp/oldlog"

def already_run():
    return os.path.exists(SQLITE_REPLAY_FILE)

def clean_up():
    retcode = subprocess.call(['rm', PID_FILE])

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
    if already_run():
        print 'you already ran this!  if you want to update, remove ' + SQLITE_REPLAY_FILE
        sys.exit(0)
    print 'not yet running... here we go!'

    replay_conn = sqlite3.connect(SQLITE_REPLAY_FILE)
    replay_db = replay_conn.cursor()
    replay_db.execute("""
            create table if not exists ip_search
            (rowid INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT,
             search TEXT, timestamp DEFAULT CURRENT_TIMESTAMP);
            """)
    replay_log = open(REPLAY_LOG_TO_READ, 'r')
    for line in replay_log:
        if not "GET /search?" in line:
            continue
        ip = line.split(' - ')[0]
        if not IP_REGEX.match(ip):
            continue
        search = prettify_search(get_search_from_line(line))

        replay_db.execute("insert into ip_search (ip, search) values ('%s', '%s')" %\
                    (ip, search.replace("'", '%%QUOTE%%')))
        replay_conn.commit()
    replay_log.close()
    replay_conn.close()
