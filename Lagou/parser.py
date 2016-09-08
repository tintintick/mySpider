# -*- coding: utf-8 -*-
from lxml import etree
import re
import json


class HTMLParser(object):

    def getinfo(self, currentpage):
        try:
            pagetree = etree.HTML(currentpage)

            nexturl = self.get_next_page_url(pagetree)

            # get current page's infos
            infos = pagetree.xpath(
                '//table[@id="ip_list"]/tr'
            )

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
        # get next_page tag
        try:
            totalpage = pagetree.xpath('//div[@class="pager_container"]/span')

        except Exception, e:
            print "get next URL error"
            print e
            return None

        return totalpage

    def parse_json(self, data, pipe):

        decoded_data = json.loads(data)
        infos = decoded_data['content']['positionResult']['result']

        for info in infos:
            item = {
                'positionName': info['positionName'],
                'positionAdvantage': info['positionAdvantage'],
                'salary': info['salary'],
                'workYear': info['workYear'],
                'companyFullName': info['companyFullName'],
                'companyLabelList': info['companyLabelList'],
                'companySize': info['companySize'],
                'businessZones': info['businessZones'],
                'city': info['city'],
                'district': info['district'],
                'education': info['education'],
                'financeStage': info['financeStage'],
                'industryField': info['industryField'],
                'createTime': info['createTime'],
                'lastLogin': info['lastLogin'],
                'score': info['score']
            }
            for key in item:
                if item[key] is None:
                    item[key] = ''
            try:
                pipe.insert_data(item)
            except Exception, e:
                print e

        pageno = decoded_data['content']['pageNo']
        print 'current page: {0}'.format(pageno)

        pagesize = decoded_data['content']['pageSize']
        totalCount = decoded_data['content']['positionResult']['totalCount']


        if totalCount % pagesize is 0:
            totalPage = totalCount / pagesize
        else:
            totalPage = totalCount / pagesize + 1

        # print 'totalPage is: {0}'.format(totalPage)

        # get position info
        # results = decoded_data['content']['positionResult']['result'][0]
        # positionName = results['positionName']
        # workYear = results['workYear']
        # education = results['education']
        # salary = results['salary']
        # positionAdvantage = results['positionAdvantage']
        # industryField = results['industryField']
        # financeStage = results['financeStage']
        # companySize = results['companySize']
        # companyFullName = results['companyFullName']
        # CreateTime = results['createTime']
        # district = results['district']
        # companyLabelList = results['companyLabelList']
        # businessZones = results['businessZones']

        return totalPage