import urllib2
from lxml import etree


class URLManager(object):
    def __init__(self):
        self.newurls = set()
        self.usedurls = set()

    def checkUrlIsNotExist(self, newurl):
        if newurl in self.newurls or newurl in self.usedurls:
            return False
        return True

    def addUrl(self, firstURL):
        if self.checkUrlIsNotExist(firstURL):
            self.newurls.add(firstURL)

    def addUrls(self, urls):
        for url in urls:
            if self.checkUrlIsNotExist(url):
                self.newurls.add(url)

    def getUrl(self):
        nexturl = self.newurls.pop()
        self.usedurls.add(nexturl)
        return nexturl


class DownLoder(object):
    def getPage(self, nexturl):
        request = urllib2.urlopen(nexturl)
        data = request.read()
        return data


class HTMLParser(object):
    def getUrls(self, currentpage):
        pageTree = etree.HTML(currentpage.lower().decode('utf-8'))
        hrefs = pageTree.xpath(u'//a')
        urls = []
        for href in hrefs:
            urls.append(href.attrib['href'])
        return urls


class OutPuter(object):
    pass


class SpiderManager(object):
    def __init__(self, firsturl):
        self.OutPuter = OutPuter()
        self.HTMLParser = HTMLParser()
        self.DownLoder = DownLoder()
        self.URLManager = URLManager()
        self.firstURL = firsturl

    def Crawl(self):
        self.URLManager.addUrl(self.firstURL)
        currenturl = self.URLManager.getUrl()
        currentpage = self.DownLoder.getPage(currenturl)
        urls = self.HTMLParser.getUrls(currentpage)
        self.URLManager.addUrls(urls)
        #data = self.HTMLParser.getData(currentpage)
        #self.OutPuter.combineData(data)
        #self.OutPuter.saveData()


#if __name__ == "__main__":
#    def main():
firsturl = "https://leohxj.gitbooks.io/a-programmer-prepares/content/effciency/coder-guide.html"
objManager = SpiderManager(firsturl)
objManager.Crawl()
