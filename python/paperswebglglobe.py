#!/usr/bin/python

import json
import re
import urllib

print "Content-type: application/json"
print

fields = ['hep-th', 'nucl-th']

institutions = ['Penn State U.', 'SLAC', 'Baja California U., Ensenada']

comma = re.compile(', ')

json_obj = []
for field in fields:
    field_res = []
    for institution in institutions:
        latitude = 0
        longitude = 0
        search_url = 'http://inspirebeta.net/search?p=fin+aff+%s+and+%s&of=id' %\
                     (urllib.quote(institution.replace(' ', '+')), urllib.quote("037:"+field))
        results = urllib.urlopen(search_url)
        results = results.readline()
        magnitude = len(comma.findall(results)) + 1

        field_res.extend([latitude, longitude, magnitude])

    json_obj.append([field, field_res])

print json.dumps(json_obj)
