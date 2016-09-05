class URLManager(object):
    def __init__(self):
        #self.newurls = set()
        """page urls need sequence"""
        self.newurls = []
        self.usedurls = set()

    def isurlexist(self, newurl):
        if newurl in self.newurls or newurl in self.usedurls:
            return False
        return True

    def addurl(self, newurl):
        if self.isurlexist(newurl):
            #self.newurls.add(firstURL)
            self.newurls.append(newurl)

    def addurls(self, newurls):
        for newurl in newurls:
            if self.isurlexist(newurl):
                self.newurls.add(newurl)

    def geturl(self):
        nexturl = self.newurls.pop(0)
        self.usedurls.add(nexturl)
        return nexturl