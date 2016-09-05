# /usr/bin/python
# -*- coding: utf-8 -*-
import time
import random
import os

import urlmanager
import downloader
import parser
import outputer


class SpiderManager(object):

    def __init__(self, starturl, baseurl, httpfile, httpsfile):
        self.starturl = starturl
        self.baseurl = baseurl
        self.httpfile = httpfile
        self.httpsfile = httpsfile
        self.URLManager = urlmanager.URLManager()
        self.DownLoder = downloader.DownLoder()
        self.HTMLParser = parser.HTMLParser()
        self.CsvOutPuter = outputer.CsvOutPuter()

    def crawl(self):

        if os.path.exists(self.httpfile):
            os.remove(self.httpfile)

        if os.path.exists(self.httpsfile):
            os.remove(self.httpsfile)

        try:
            # add columns to csv file
            features = ("url", "speed", "ctime", "ltime")
            self.CsvOutPuter.outputtocsv(features, self.httpfile)
            self.CsvOutPuter.outputtocsv(features, self.httpsfile)

            self.URLManager.addurl(self.starturl)

            while True:
                time.sleep(random.randint(1, 3))
                currenturl = self.URLManager.geturl()

                # static page
                currentpage = self.DownLoder.getpage(currenturl)

                # dynamic page
                # currentpage = self.DownLoder.get_dynamic_page(currenturl)

                if currentpage is not None:
                    httpitems, httpsitems, nexturl = self.HTMLParser.getinfo(currentpage)
                    print nexturl
                    # items = self.HTMLParser.getinfo(currentpage)

                    for item in httpitems:
                        self.CsvOutPuter.outputtocsv(item, self.httpfile)

                    for item in httpsitems:
                        self.CsvOutPuter.outputtocsv(item, self.httpsfile)

                    if nexturl is not None:
                        self.URLManager.addurl(self.baseurl + nexturl)
                    else:
                        print "crawling is over"
                        break

                else:
                    print currenturl + " contains no content!"
                    break

        except Exception, e:
            print e


url_start = "http://www.xicidaili.com/nn"
url_base = "http://www.xicidaili.com"
http_filename = "http_proxy.csv"
https_filename = "https_proxy.csv"

obj_manager = SpiderManager(url_start, url_base, http_filename, https_filename)
obj_manager.crawl()