import urllib2
import re
try:
    from pyteaser import SummarizeUrl
except ImportError:
    print "The Pyteaser library is required to use"
    print "It can be downloaded here: https://github.com/xiaoxu193/PyTeaser"
    exit()


class ScrapeTorontoStar:
    
    def __init__(self, searchTerms):
        self.searchTerms = searchTerms
    
    def printSummaries(self):
        outputFile = open ("Toronto Star Summaries.txt", "w")
        for term in self.searchTerms:
            outputFile.write("SEARCHTERM: " + term + "\n")
            
            term = term.replace(" ", "+")
            response = urllib2.urlopen("http://www.thestar.com/search.html?q=" + term)
            source = response.read()
            source = source.replace(" ", "")
            source = source.replace("\t", "")
            hi = source.split("\n")
            k = 0
            fileTest = 1
            try:
                file = open (term + "TorontoStarMostRecentUrl", "r")
            except Exception, e:
                mostRecent = ""
                fileTest = 0
            if fileTest == 1:
                mostRecent = file.readline()
                file.close()
        
            hold = ""
            
            for i in hi:
                #Line in Toronto Star source code that comes directly after last article
                if (i == '<divclass="fromthehomepagesection">'):
                    break
                potentialArticles = re.search('^<ahref=.+\.html">$', i)
                if hasattr (potentialArticles, 'group'):
                    articleUrl = potentialArticles.group(0)
                    #Cleans up the beginning and end of the url
                    articleUrl = articleUrl.replace('<ahref="', "")
                    articleUrl = articleUrl.replace('">', "")
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
                file = open (term + "TorontoStarMostRecentUrl", "w")
                file.write(hold)
                file.close()
            outputFile.write("\n\n\n\n\n")
            print "Toronto Star: " + term.replace("+", " ") + " is done."
        outputFile.close()