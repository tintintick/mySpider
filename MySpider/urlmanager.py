class URLManager(object):
    def __init__(self):
        #self.newurls = set()
        """page urls need sequence"""
        self.newurls = []
        self.usedurls = set()

    def checkurlisnotexist(self, newurl):
        if newurl in self.newurls or newurl in self.usedurls:
            return False
        return True

    def addurl(self, firstURL):
        if self.checkurlisnotexist(firstURL):
            #self.newurls.add(firstURL)
            self.newurls.append(firstURL)

    def addurls(self, urls):
        for url in urls:
            if self.checkurlisnotexist(url):
                self.newurls.add(url)
                #self.newurls.append(url)

    def geturl(self):
        nexturl = self.newurls.pop(0)
        self.usedurls.add(nexturl)
        return nexturl