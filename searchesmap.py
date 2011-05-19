#!/usr/bin/python

from pygeoip import GeoIP
import re
import sys

GI = GeoIP("/home/valkyrie/projects/inspire-log-viz/src/GeoLiteCity.dat")
LOG_TO_READ = "/home/valkyrie/projects/inspire-log-viz/log.sample"
IP_REGEX = re.compile(r'(\d{1,3}.){4}')

def get_lat_long_pair(ip):
    record = GI.record_by_addr(ip)
    if not record:
        return (0,0)
    return (record['latitude'], record['longitude'])

def pull_ip_list_from_log():
    log = open(LOG_TO_READ)
    ips = []
    for line in log:
        if not "GET /search?" in line:
            continue
        ip = line.split(' - ')[0]
        if IP_REGEX.match(ip):
            ips.append(ip)
    return ips

ips = pull_ip_list_from_log()
for ip in ips:
    latitude, longitude = get_lat_long_pair(ip)
    print str(latitude) + ' ' + str(longitude)
