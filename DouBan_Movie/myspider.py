# /usr/bin/python
# coding:utf-8
import urlmanager
import downloader
import parser
import outputer


class SpiderManager(object):
    def __init__(self, starturl, baseurl, filename):
        self.starturl = starturl
        self.baseurl = baseurl
        self.filename = filename
        self.URLManager = urlmanager.URLManager()
        self.DownLoder = downloader.DownLoder()
        self.HTMLParser = parser.HTMLParser()
        self.CsvOutPuter = outputer.CsvOutPuter()

    def crawl(self):

        try:
            #add columns to csv file
            indexs = ("index", "title", "star", "staff", "classification", "quote")
            self.CsvOutPuter.outputtocsv(indexs, self.filename)

            self.URLManager.addurl(self.starturl)

            while True:
                currenturl = self.URLManager.geturl()
                currentpage = self.DownLoder.getpage(currenturl)

                if currentpage is not None:
                    # urls = self.HTMLParser.getUrls(currentpage)
                    items, nexturl = self.HTMLParser.getpagedata(currentpage)
                    for item in items:
                        self.CsvOutPuter.outputtocsv(item, self.filename)

                    if nexturl is not None:
                        nexturl = self.baseurl + nexturl
                        self.URLManager.addurl(nexturl)
                    else:
                        break

        except Exception, e:
            print e

            # data = self.HTMLParser.getData(currentpage)
            # self.OutPuter.combineData(data)
            # self.OutPuter.saveData()


#if __name__ == "__main__":
#    def main():
url_start = "https://movie.douban.com/top250"
url_base = "https://movie.douban.com/top250"
outputfilename = "output.csv"

objmanager = SpiderManager(url_start, url_base, outputfilename)
objmanager.crawl()
