import requests
from lxml import etree
import csv
import re


class DouBanItem(object):
    def __init__(self):
        self.index = 0
        self.title = 0
        self.staff = 0
        self.classification = 0
        self.star = 0
        self.quote = 0


class URLManager(object):
    def __init__(self):
        #self.newurls = set()
        """page urls need sequence"""
        self.newurls = []
        self.usedurls = set()

    def checkUrlIsNotExist(self, newurl):
        if newurl in self.newurls or newurl in self.usedurls:
            return False
        return True

    def addUrl(self, firstURL):
        if self.checkUrlIsNotExist(firstURL):
            #self.newurls.add(firstURL)
            self.newurls.append(firstURL)

    def addUrls(self, urls):
        for url in urls:
            if self.checkUrlIsNotExist(url):
                self.newurls.add(url)
                #self.newurls.append(url)

    def getUrl(self):
        nexturl = self.newurls.pop(0)
        self.usedurls.add(nexturl)
        return nexturl


class DownLoder(object):
    def getPage(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            data = request.text
            return data
        else:
            return None


class HTMLParser(object):
    def getUrls(self, currentpage):
        pass

    def getPageData(self, currentpage, baseurl, filename):

        try:
            pageTree = etree.HTML(currentpage)#.lower().decode('utf-8'))

            """get current page's info"""
            movies = pageTree.xpath(
                '//ol[@class="grid_view"]/li/div[@class="item"]'
            )

            for movie in movies:
                item = DouBanItem()
                """index"""
                item.index = movie.xpath(
                    'div[@class="pic"]/em/text()'
                )[0]

                # header
                """title"""
                item.title = movie.xpath(
                    'div[@class="info"]/div[@class="hd"]/a/span[@class="title"]/text()'
                )[0]

                # body
                """staff"""
                item.staff = movie.xpath(
                    'div[@class="info"]/div[@class="bd"]/p/text()'
                )[0]

                """classification"""
                item.classification = movie.xpath(
                    'div[@class="info"]/div[@class="bd"]/p/text()'
                )[1]

                """star"""
                item.star = movie.xpath(
                    'div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()'
                )[0]

                """quote"""
                try:
                    item.quote = movie.xpath(
                        'div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()'
                    )[0]
                except Exception,e:
                    item.quote = ""

                itemdic = {"index":item.index, "title":item.title.encode('utf-8'), "classification":item.classification.encode('utf-8'), "staff":item.staff.encode('utf-8'), "star":item.star, "quote":item.quote.encode('utf-8')}

                for item in itemdic:
                    itemdic[item] = re.sub('\n', '', itemdic[item])
                    itemdic[item] = re.sub(' +', ' ', itemdic[item])

                """output"""
                itemdata = (itemdic["index"], itemdic["title"], itemdic["star"], itemdic["staff"], itemdic["classification"], itemdic["quote"])
                OutPuter().outPutToCsv(itemdata, filename)

            """get next page's url"""
            try:
                nextpageurl = baseurl + pageTree.xpath('//span[@class="next"]/a/@href')[0]
            except Exception, e:
                return None

        except Exception, e:
            print e
            return nextpageurl

        return nextpageurl



class OutPuter(object):
    def outPutToCsv(self, data, filename):
        fobj = file(filename, "a")
        writer = csv.writer(fobj)
        writer.writerow(data)
        fobj.close()


class SpiderManager(object):
    def __init__(self, starturl, baseurl, filename):
        self.startUrl = starturl
        self.baseUrl = baseurl
        self.fileName = filename
        self.URLManager = URLManager()
        self.DownLoder = DownLoder()
        self.HTMLParser = HTMLParser()
        self.OutPuter = OutPuter()

    def Crawl(self):

        try:
            indexs = ("index", "title", "star", "staff", "classification", "quote")
            self.OutPuter.outPutToCsv(indexs, self.fileName)

            self.URLManager.addUrl(self.startUrl)
            while True:
                currenturl = self.URLManager.getUrl()
                currentpage = self.DownLoder.getPage(currenturl)
                nextpageurl = 0
                if currentpage != None:
                    # urls = self.HTMLParser.getUrls(currentpage)
                    nextpageurl = self.HTMLParser.getPageData(currentpage, self.baseUrl, self.fileName)
                    if nextpageurl is not None:
                        self.URLManager.addUrl(nextpageurl)
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
objManager.Crawl()
