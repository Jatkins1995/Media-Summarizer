#!/usr/bin/python

import urllib2
import re
try:
    from pyteaser import SummarizeUrl
except ImportError:
    print "The Pyteaser library is required to use"
    print "It can be downloaded here: https://github.com/xiaoxu193/PyTeaser"
    exit()

class ScrapeGlobeAndMail:

    def __init__(self, searchTerms):
        self.searchTerms = searchTerms

    def printSummaries(self):

        outputFile = open ("Globe and Mail Summaries.txt", "w")

        for term in self.searchTerms:
            outputFile.write("SEARCHTERM: " + term + "\n")
            
            term = term.replace(" ", "+")
            response = urllib2.urlopen("http://theglobeandmail.com/search/?q=" + term)
            source = response.read()
            source = source.replace(" ", "")
            source = source.replace("\t", "")
            sourceLines = source.split("\n")
            fileTest = 1
            try:
                file = open (term + "GlobeAndMailMostRecentUrl", "r")
            except Exception, e:
                mostRecent = ""
                fileTest = 0
            if fileTest == 1:
                mostRecent = file.readline()
                file.close()

            hold = ""
            k = 0

            searchStatus = 0;

            for i in sourceLines:
                if searchStatus == 0:
                    if i == '<aname="newsResults"></a>':
                        searchStatus = 1
                if searchStatus == 1:
                    if i == '<ulclass="pagination">':
                        break
                    else:
                        potentialArticles = re.search('<h3>.+</h3>', i)
                        if hasattr (potentialArticles, 'group'):
                            articleUrl = potentialArticles.group(0)
                            articleUrl = articleUrl.replace('<h3><ahref="', "")
                            splitUrl = articleUrl.split('">')
                            articleUrl = "http://www.theglobeandmail.com" + splitUrl[0]
                            if (articleUrl == mostRecent):
                                if k == 0:
                                    hold = mostRecent
                                    outputFile.write("No new articles")
                                break
                            if (k == 0):
                                hold = articleUrl
                                k = 1
                            summary = SummarizeUrl(articleUrl)
                            outputFile.write("\n\n")
                            outputFile.write(articleUrl + "\n\n")
                            if summary is None:
                                outputFile.write("Unable to summarize")
                            else:
                                for lineOfSummery in summary:
                                    lineOfSummery = lineOfSummery.replace("\n", "")
                                    outputFile.write(lineOfSummery.encode('utf8') + "\n")
            if (hold != ""):
                file = open (term + "GlobeAndMailMostRecentUrl", "w")
                file.write(hold)
                file.close()
            outputFile.write("\n\n\n\n\n")
            print "Globe And Mail: " + term.replace("+", " ") + " is done."
        outputFile.close()