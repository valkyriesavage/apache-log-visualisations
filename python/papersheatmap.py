#!/usr/bin/python

INST_FILE = '/opt/viz/insts.psv'

import json
import re
import urllib

insts = open(INST_FILE)
institutions = []
for line in insts:
    institutions.append(line.replace('\n', '').split('|'))

comma = re.compile(', ')

json_obj = []
for institution in institutions:
    if not len(institution) == 3:
        print 'something is wrong with ' + str(institution)
        continue
    inst_name, long_name, coords = institution
    if not ',' in coords:
        print inst_name + ' has invalid coordinates'
        continue
    latitude, longitude = coords.split(',')
    search_url = 'https://insplnx1.slac.stanford.edu/search?p=fin+aff+%s&of=id' %\
                     (urllib.quote(inst_name.replace(' ', '+')))
    results = urllib.urlopen(search_url)
    results = results.readline()
    count = len(comma.findall(results)) + 1
    json_obj.append({
            'institution' : long_name,
            'latitude' : latitude,
            'longitude' : longitude,
            'count' : count
            })

print json.dumps(json_obj)
