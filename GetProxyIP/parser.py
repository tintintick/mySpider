# -*- coding: utf-8 -*-
from lxml import etree
import re


class HTMLParser(object):
    def geturls(self, currentpage):
        pass

    def getinfo(self, currentpage):
        try:
            pagetree = etree.HTML(currentpage)

            # get current page's infos
            infos = pagetree.xpath(
                '//table[@id="ip_list"]/tr'
            )

            nexturl = self.get_next_page_url(pagetree)

            httplist = []
            httpslist = []

            for info in infos[1:]:

                tds = info.xpath(
                    'td'
                )

                itemdict = {}

                # ip
                ip = tds[1].text

                # port
                port = tds[2].text

                # protocol
                protocol = tds[5].text

                # proxy url
                itemdict["url"] = "{pro}://{ip}:{port}".format(pro=protocol.lower(), ip=ip, port=port)

                # speed
                itemdict["speed"] = (tds[6].xpath(
                    './div/@title'
                ))[0]

                # connecting time
                itemdict["ctime"] = (tds[7].xpath(
                    'div/@title'
                ))[0]

                # living time
                itemdict["ltime"] = tds[8].text

                # convert living time into minute
                if u'分钟' in itemdict['ltime']:
                    ltime = int(re.sub(u'分钟', '', itemdict['ltime'])) * 60
                    itemdict['ltime'] = ltime

                elif u'小时' in itemdict['ltime']:
                    ltime = int(re.sub(u'小时', '', itemdict['ltime'])) * 60 * 60
                    itemdict['ltime'] = ltime

                elif u'天' in itemdict['ltime']:
                    ltime = int(re.sub(u'天', '', itemdict['ltime'])) * 24 * 60 * 60
                    itemdict['ltime'] = ltime

                else:
                    pass

                itemdict['speed'] = re.sub(u'秒', '', itemdict['speed'])
                itemdict['ctime'] = re.sub(u'秒', '', itemdict['ctime'])
                itemdict['speed'] = float(itemdict["speed"].encode('utf-8'))
                itemdict['ctime'] = float(itemdict["ctime"].encode('utf-8'))
                itemdict['ltime'] = int(itemdict["ltime"])

                if itemdict['ltime'] <= 30 * 24 * 60 * 60 or itemdict['ctime'] >= 0.05 or itemdict['speed'] >= 0.3:
                    continue

                # metadata
                itemdata = (
                    itemdict["url"],
                    itemdict['speed'],
                    itemdict['ctime'],
                    itemdict['ltime']
                )

                if protocol.lower() is 'http':
                    httplist.append(itemdata)
                else:
                    httpslist.append(itemdata)

        except Exception, e:
            print e
            return httplist, httpslist, None

        return httplist, httpslist, nexturl

    def get_next_page_url(self, pagetree):
        # get next page
        try:
            nexturl = pagetree.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href')[0]

        except Exception, e:
            print "get next URL error"
            print e
            return None

        return nexturl
