#!/usr/bin/python

import re
import urllib

from invenio.search_engine_query_parser import SpiresToInvenioSyntaxConverter

stisc = SpiresToInvenioSyntaxConverter()

SEARCH_LEAD = re.compile('GET /search?')
SEARCH = re.compile('(p|p1)=(?P<term>.*?)(&| )')

RM_CITE = re.compile('rm=citation')

INV = re.compile('(%3a|%3A|:)')
SPI = re.compile('^(f|fin|find) ')
AUTH = re.compile('^(a|author|au) ')
ANY_AUTH = re.compile('(a|author|au)(:| )')
CITE_SOMETHING = re.compile('(citesummary|refersto|citedby|cited|topcite)')
TITLE = re.compile('(t|title)(:| )')
AFF = re.compile('(aff|affiliation)(:| )')
AUTH_INV = re.compile('^author:')
REC = re.compile('recid:')
ARX = re.compile('arxiv:')
PAREN = re.compile('\(|\)')
NESTED_PAREN = re.compile('\([^\)]*\(')

MAIN_PAGE = re.compile('^http://inspirebeta.net/$')
OTHER_INSPIRE = re.compile('^http://inspirebeta.net/')
AUTHOR_PAGE = re.compile('inspirebeta.net/author/')
CITE_SUMMARY = re.compile('&of=hcs')

invenio = 0
inv_with_find = 0
recid = 0
arxiv = 0
spires_find = 0
naked_author = 0
naked_author_inv = 0
inv_author = 0
naked_other = 0
other = 0
paren = 0
nested_paren = 0
total = 0

referred_from_author_page = 0
referred_from_hcs = 0

main_page = 0
other_inspire = 0
scary_outside_world = 0
no_referrer = 0

any_auth = 0
cite_something = 0
title = 0
aff = 0

inv_from_cite_summary = 0
spi_from_cite_summary = 0
other_from_cite_summary = 0

f = open('/opt/viz/log.bigsample')
for line in f:

    if not SEARCH_LEAD.search(line) or not SEARCH.search(line):
        continue

    referrer = line.split('"')[3]
    search_term = urllib.unquote(SEARCH.search(line).group('term').lower().replace('+', ' '))

    if MAIN_PAGE.match(referrer):
        main_page += 1
    elif OTHER_INSPIRE.match(referrer):
        other_inspire += 1
    elif not '-' == referrer:
        scary_outside_world += 1
    else:
        no_referrer += 1

    if AUTHOR_PAGE.search(referrer):
        referred_from_author_page += 1
        #continue
    if CITE_SUMMARY.search(referrer):
        referred_from_hcs += 1
        if SPI.search(search_term) or AUTH.search(search_term):
            spi_from_cite_summary += 1
        elif INV.search(search_term.replace('cited:', 'c').replace('collection:', 'cc')):
            inv_from_cite_summary += 1
        else:
            other_from_cite_summary += 1
        #continue

    total += 1

    if ANY_AUTH.search(search_term) or AUTHOR_PAGE.search(referrer):
        any_auth += 1
    if CITE_SOMETHING.search(search_term) or CITE_SUMMARY.search(referrer) or RM_CITE.search(line):
        cite_something += 1
    if AFF.search(search_term):
        aff += 1
    if TITLE.search(search_term):
        title += 1

    if SPI.search(search_term):
        spires_find += 1
    elif AUTH.search(search_term):
        naked_author += 1
        if INV.search(search_term):
            naked_author_inv += 1
    elif search_term.split(' ')[0] in stisc._SPIRES_TO_INVENIO_KEYWORDS_MATCHINGS.keys():
        naked_other += 1
    elif INV.search(search_term):
        invenio += 1
        if REC.search(search_term):
            recid += 1
            '''if re.search('(^recid):', search_term):
                print search_term'''
        elif ARX.search(search_term):
            arxiv += 1
    else:
        other += 1
    if AUTH_INV.search(search_term):
        inv_author += 1
    if SPI.search(search_term) and INV.search(search_term):
        inv_with_find += 1
    if PAREN.search(search_term):
        paren += 1
        if NESTED_PAREN.search(search_term):
            nested_paren += 1

f.close()

print 'main page searches : ' + str(main_page)
print 'other inspire page searches : ' + str(other_inspire)
print 'searches coming from someplace else : ' + str(scary_outside_world)
print 'searches without a referrer : ' + str(no_referrer)
print
print

print 'referred from author page : ' + str(referred_from_author_page)
print 'referred from cite summary : ' + str(referred_from_hcs)
print ' *** spires : ' + str(spi_from_cite_summary)
print ' *** invenio : ' + str(inv_from_cite_summary)
print ' *** other : ' + str(other_from_cite_summary)

print
print
print 'any kind of author search : ' + str(any_auth)
print 'any kind of citation search : ' + str(cite_something)
print 'title searches : ' + str(title)
print 'affiliation searches : ' + str(aff)
print

print 'invenio : %d (recid : %d, arXiv : %d, pure invenio : %d)\nspires : %d\nnaked author : %d (with invenio : %d)\ninvenio author search : %d\nnaked other : %d\nother : %d\ninvenio with find : %d\nparens : %d (nested : %d)\ntotal : %d\n' %\
          (invenio, recid, arxiv, (invenio-recid-arxiv),  spires_find, naked_author, naked_author_inv, inv_author, naked_other, other, inv_with_find, paren, nested_paren, total)
