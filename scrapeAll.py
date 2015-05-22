#!/usr/bin/python


import urllib2
from scrapeGlobeAndMail import ScrapeGlobeAndMail
from scrapeTorontoStar import ScrapeTorontoStar
import re
try:
    from pyteaser import SummarizeUrl
except ImportError:
    print "The Pyteaser library is required to use"
    print "It can be downloaded here: https://github.com/xiaoxu193/PyTeaser"
    exit()

input = "a"
list = []

while input != "go":

    input = raw_input('Type a single search term then press enter please.\nType go then hit enter to begin summarizing.\nPlease note that any old summary file will be deleted.\n> ')

    if input != "go":
        list.append(input)

TorontoStar = ScrapeTorontoStar(list)
GlobeAndMail = ScrapeGlobeAndMail(list)
print "Terms are: "
for i in TorontoStar.searchTerms:
    print i

TorontoStar.printSummaries()
GlobeAndMail.printSummaries()