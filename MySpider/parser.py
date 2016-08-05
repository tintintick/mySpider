from lxml import etree
import re


class HTMLParser(object):
    def geturls(self, currentpage):
        pass

    def getpagedata(self, currentpage):
        try:
            pagetree = etree.HTML(currentpage)#.lower().decode('utf-8'))
            """get current page's movies"""
            movies = pagetree.xpath(
                '//ol[@class="grid_view"]/li/div[@class="item"]'
            )

            movielist = []
            for movie in movies:
                itemdict = {}
                """index"""
                itemdict["index"] = movie.xpath(
                    'div[@class="pic"]/em/text()'
                )[0]

                # header
                # title
                itemdict["title"] = movie.xpath(
                    'div[@class="info"]/div[@class="hd"]/a/span[@class="title"]/text()'
                )[0].encode('utf-8')

                # body
                # staff
                itemdict["staff"] = movie.xpath(
                    'div[@class="info"]/div[@class="bd"]/p/text()'
                )[0].encode('utf-8')

                # classification
                itemdict["classification"] = movie.xpath(
                    'div[@class="info"]/div[@class="bd"]/p/text()'
                )[1].encode('utf-8')

                # star
                itemdict["star"] = movie.xpath(
                    'div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()'
                )[0]

                # quote
                try:
                    itemdict["quote"] = movie.xpath(
                        'div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()'
                    )[0].encode('utf-8')
                except Exception, e:
                    itemdict["quote"] = ""

                for item in itemdict:
                    itemdict[item] = re.sub('\n', '', itemdict[item])
                    itemdict[item] = re.sub(' +', ' ', itemdict[item])

                # metadata
                itemdata = (
                    itemdict["index"],
                    itemdict["title"],
                    itemdict["star"],
                    itemdict["staff"],
                    itemdict["classification"],
                    itemdict["quote"]
                )

                movielist.append(itemdata)

            # get next page
            try:
                nexturl = pagetree.xpath('//span[@class="next"]/a/@href')[0]
            except Exception, e:
                print e
                return movielist, None

        except Exception, e:
            print e
            return movielist, nexturl

        return movielist, nexturl
