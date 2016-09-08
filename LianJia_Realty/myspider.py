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

    def __init__(self, starturl, baseurl, filename):
        self.starturl = starturl
        self.baseurl = baseurl
        self.filename = filename
        self.URLManager = urlmanager.URLManager()
        self.DownLoder = downloader.DownLoder()
        self.HTMLParser = parser.HTMLParser()
        self.CsvOutPuter = outputer.CsvOutPuter()

    def crawl(self):

        logpath = './deal_chaoyang.csv'
        if os.path.exists(logpath):
            os.remove(logpath)
        # try:
        # currentpage = self.DownLoder.getpage("http://bj.lianjia.com/chengjiao/chaoyang")
        # except Exception,e:
        #     print e

        try:
            # add columns to csv file
            features = ("name", "type", "square", "direction", "furnish", "totalprice", "unitprice", "floortype", "floors", "year", "structure", "dealdate", "other")
            self.CsvOutPuter.outputtocsv(features, self.filename)

            self.URLManager.addurl(self.starturl)

            # nextnum = 2
            while True:
                time.sleep(random.randint(1, 3))
                currenturl = self.URLManager.geturl()

                # static page
                currentpage = self.DownLoder.getpage(currenturl)

                # dynamic page
                # currentpage = self.DownLoder.get_dynamic_page(currenturl)

                if currentpage is not None:
                    items, nexturl = self.HTMLParser.getinfo(currentpage)
                    print nexturl
                    # items = self.HTMLParser.getinfo(currentpage)

                    for item in items:
                        self.CsvOutPuter.outputtocsv(item, self.filename)

                    if nexturl is not None:
                        self.URLManager.addurl(self.baseurl + nexturl)
                    # if nextnum <= 100:
                    #     self.URLManager.addurl(self.baseurl + "/chengjiao/chaoyang/pg" + str(nextnum))
                    #     nextnum += 1
                    #     print nextnum
                    else:
                        break

                else:
                    print currenturl + "contains no content!"
                    break

        except Exception, e:
            print e


url_start = "http://bj.lianjia.com/chengjiao/chaoyang/"
url_base = "http://bj.lianjia.com"
output_filename = "deal_chaoyang.csv"

obj_manager = SpiderManager(url_start, url_base, output_filename)
obj_manager.crawl()