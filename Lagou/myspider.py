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

    def __init__(self, starturl, pagenum):
        self.starturl = starturl
        self.pagenum = int(pagenum)
        self.URLManager = urlmanager.URLManager()
        self.DownLoder = downloader.DownLoder()
        self.HTMLParser = parser.HTMLParser()

    def crawl(self):

        # if os.path.exists(self.filename):
        #     os.remove(self.filename)

        try:
            # add columns to csv file
            # features = ("url", "speed", "ctime", "ltime")
            # self.CsvOutPuter.outputtocsv(features, self.filename)
            # self.URLManager.addurl(self.starturl)

            # use mongodb to store data
            pipe = outputer.MongodbPipe('lagou_position', 'python_bejing')

            while True:
                time.sleep(random.randint(1, 3))
                # currenturl = self.URLManager.geturl()

                # static page
                json_page = self.DownLoder.get_page_via_post(self.starturl, self.pagenum)

                # dynamic page
                # currentpage = self.DownLoder.get_dynamic_page(currenturl)

                if json_page is not None:
                    totalpage = self.HTMLParser.parse_json(json_page, pipe)

                    if self.pagenum <= totalpage:
                        self.pagenum += 1
                    else:
                        print "crawling is over"
                        break

                else:
                    print " contains no content!"
                    break

        except Exception, e:
            print e


url_start = "http://www.lagou.com/jobs/positionAjax.json?px=new&city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false"
first_pagenum = "1"

obj_manager = SpiderManager(url_start, first_pagenum)
obj_manager.crawl()