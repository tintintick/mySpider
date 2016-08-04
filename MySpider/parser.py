from lxml import etree
import re
import items

class HTMLParser(object):
    def geturls(self, currentpage):
        pass

    def getpagedata(self, currentpage, baseurl, filename):

        try:
            pageTree = etree.HTML(currentpage)#.lower().decode('utf-8'))

            """get current page's info"""
            movies = pageTree.xpath(
                '//ol[@class="grid_view"]/li/div[@class="item"]'
            )

            for movie in movies:
                item = items.DouBanItem()
                """index"""
                item.index = movie.xpath(
                    'div[@class="pic"]/em/text()'
                )[0]

                # header
                """title"""
                item.title = movie.xpath(
                    'div[@class="info"]/div[@class="hd"]/a/span[@class="title"]/text()'
                )[0]

                # body
                """staff"""
                item.staff = movie.xpath(
                    'div[@class="info"]/div[@class="bd"]/p/text()'
                )[0]

                """classification"""
                item.classification = movie.xpath(
                    'div[@class="info"]/div[@class="bd"]/p/text()'
                )[1]

                """star"""
                item.star = movie.xpath(
                    'div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()'
                )[0]

                """quote"""
                try:
                    item.quote = movie.xpath(
                        'div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()'
                    )[0]
                except Exception,e:
                    item.quote = ""

                itemdic = {"index":item.index, "title":item.title.encode('utf-8'), "classification":item.classification.encode('utf-8'), "staff":item.staff.encode('utf-8'), "star":item.star, "quote":item.quote.encode('utf-8')}

                for item in itemdic:
                    itemdic[item] = re.sub('\n', '', itemdic[item])
                    itemdic[item] = re.sub(' +', ' ', itemdic[item])

                """output"""
                itemdata = (itemdic["index"], itemdic["title"], itemdic["star"], itemdic["staff"], itemdic["classification"], itemdic["quote"])
                OutPuter().outputtocsv(itemdata, filename)

            """get next page's url"""
            try:
                nextpageurl = baseurl + pageTree.xpath('//span[@class="next"]/a/@href')[0]
            except Exception, e:
                return None

        except Exception, e:
            print e
            return nextpageurl

        return nextpageurl
