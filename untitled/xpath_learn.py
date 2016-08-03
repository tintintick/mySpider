import requests
from lxml import etree
from urlparse import urljoin

class XpathLearn(object):
    def __init__(self, starturl, baseurl):
        self.start_url = starturl
        self.base_url = baseurl

    def getUrlFromHomePage(self):
        try:
            result = open("result.log", "w")
            response = requests.get(self.start_url)
            page = etree.HTML(response.text)
            articles = page.xpath('//div[@class="content_container"]/div[@class="post"]')
            #hrefs = page.xpath('//a')
            for article in articles:
                title = article.xpath('h2/a/text()')[0]
                posttime = article.xpath('div[@class="post-meta"]/text()')[0]
                relativeurl = article.xpath('p[@class="readmore"]/a/@href')[0]
                absurl = urljoin(self.base_url, relativeurl)
                print absurl
                result.write(absurl+'\n')

        except Exception, a:
            print a

        finally:
            result.close()
            return


test = XpathLearn("http://www.pycoding.com", "http://www.pycoding.com")
test.getUrlFromHomePage()