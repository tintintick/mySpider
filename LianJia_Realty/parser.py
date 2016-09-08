# -*- coding: utf-8 -*-
from lxml import etree
import re


class HTMLParser(object):
    def geturls(self, currentpage):
        pass

    def getinfo(self, currentpage):
        try:
            pagetree = etree.HTML(currentpage)

            # get current page's rooms
            rooms = pagetree.xpath(
                '//ul[@class="listContent"]/li/div[@class="info"]'
            )

            roomlist = []
            for room in rooms:
                itemdict = {}

                # title
                itemdict["title"] = room.xpath(
                    'div[@class="title"]/a/text()'
                )[0]

                # house_info
                itemdict["house_info"] = room.xpath(
                    'div[@class="address"]/div[@class="houseInfo"]/text()'
                )[0]

                # total_price
                itemdict["total_price"] = room.xpath(
                    'div[@class="address"]/div[@class="totalPrice"]/span/text()'
                )[0]

                # unit_price
                itemdict["unit_price"] = room.xpath(
                    'div[@class="flood"]/div[@class="unitPrice"]/span/text()'
                )[0]

                # position_info
                itemdict["position_info"] = room.xpath(
                    'div[@class="flood"]/div[@class="positionInfo"]/text()'
                )[0]

                # deal_date
                itemdict["deal_date"] = room.xpath(
                    'div[@class="address"]/div[@class="dealDate"]/text()'
                )[0]

                # source
                itemdict["source"] = room.xpath(
                    'div[@class="flood"]/div[@class="source"]/text()'
                )[0]

                # other
                itemdict["other"] = ""
                try:
                    other = room.xpath(
                        'div[@class="dealHouseInfo"]/span[@class="dealHouseTxt"]//span/text()'
                    )

                    for txt in other:
                        itemdict["other"] = itemdict["other"] + "/" + txt

                except:
                    itemdict["other"] = ""

                for item in itemdict:
                    itemdict[item] = re.sub('\(', ' ', itemdict[item])
                    itemdict[item] = re.sub('\)', '', itemdict[item])
                    itemdict[item] = re.sub('\n', '', itemdict[item])
                    itemdict[item] = re.sub(' +', ' ', itemdict[item])
                itemdict["position_info"] = re.sub(u'建', ' ', itemdict["position_info"])

                # metadata
                try:
                    titleinfo = itemdict["title"].encode("utf-8").split(' ')
                    itemdict["name"] = titleinfo[0]
                    itemdict["type"] = titleinfo[1]
                    itemdict["square"] = titleinfo[2]
                except Exception, e:
                    print "titleinfo"
                    print e
                    print titleinfo

                try:
                    houseinfo = itemdict["house_info"].encode("utf-8").split('|')
                    itemdict["direction"] = houseinfo[0]
                    itemdict["furnish"] = houseinfo[1]
                except Exception, e:
                    print "houseinfo"
                    print e
                    print houseinfo

                try:
                    positioninfo = itemdict["position_info"].encode("utf-8").split(' ')
                    itemdict["floor_type"] = positioninfo[0] if len(positioninfo) >= 1 else ""
                    itemdict["floors"] = positioninfo[1] if len(positioninfo) >= 2 else ""
                    itemdict["year"] = positioninfo[2] if len(positioninfo) >= 3 else ""
                    itemdict["structure"] = positioninfo[3] if len(positioninfo) == 4 else ""
                except Exception, e:
                    print "positioninfo"
                    print e
                    print itemdict["position_info"]

                itemdata = (
                    itemdict["name"],
                    itemdict["type"],
                    itemdict["square"],
                    itemdict["direction"],
                    itemdict["furnish"],
                    itemdict["total_price"],
                    itemdict["unit_price"],
                    itemdict["floor_type"],
                    itemdict["floors"],
                    itemdict["year"],
                    itemdict["structure"],
                    itemdict["deal_date"].encode("utf-8"),
                    itemdict["other"].encode("utf-8")
                )

                roomlist.append(itemdata)

            # get next page
            try:
                page_data = pagetree.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')[0]
                pagenums = re.findall("\d+", page_data, flags=0)
                if int(pagenums[1]) + 1 <= int(pagenums[0]):
                    nexturl = "/chengjiao/chaoyang/pg" + str(int(pagenums[1]) + 1)

            except Exception, e:
                # f = open("/home/redhat/Desktop/test.log", "w")
                # f.write(currentpage)
                # f.close()
                print "get next page error"
                print e
                return roomlist, None

        except Exception, e:
            print e
            return roomlist, None

        return roomlist, nexturl
