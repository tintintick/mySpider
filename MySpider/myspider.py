import urlmanager
import downloader
import parser
import outputer



class SpiderManager(object):
    def __init__(self, starturl, baseurl, filename):
        self.startUrl = starturl
        self.baseUrl = baseurl
        self.fileName = filename
        self.URLManager = urlmanager.URLManager()
        self.DownLoder = downloader.DownLoder()
        self.HTMLParser = parser.HTMLParser()
        self.OutPuter = outputer.CsvOutPuter()

    def crawl(self):

        try:
            #add columns to csv file
            indexs = ("index", "title", "star", "staff", "classification", "quote")
            self.OutPuter.outputtocsv(indexs, self.fileName)

            self.URLManager.addurl(self.startUrl)

            while True:
                currenturl = self.URLManager.geturl()
                currentpage = self.DownLoder.getpage(currenturl)
                nextpageurl = 0
                if currentpage != None:
                    # urls = self.HTMLParser.getUrls(currentpage)
                    nextpageurl = self.HTMLParser.getpagedata(currentpage, self.baseUrl, self.fileName)
                    if nextpageurl is not None:
                        self.URLManager.addurl(nextpageurl)
                    else:
                        break

        except Exception, e:
            print e

            # data = self.HTMLParser.getData(currentpage)
            # self.OutPuter.combineData(data)
            # self.OutPuter.saveData()


# if __name__ == "__main__":
#    def main():
starturl = "https://movie.douban.com/top250"
baseurl = "https://movie.douban.com/top250"
outputfilename = "output.csv"

objManager = SpiderManager(starturl, baseurl, outputfilename)
objManager.crawl()
