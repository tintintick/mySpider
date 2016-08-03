#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc :
"""
from coolscrapy.items import HuxiuItem
import scrapy


class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = [
        "http://www.huxiu.com"
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="mod-info-flow"]/div[@class="mod-b mod-art "]/div[@class="mob-ctt"]'):
            #item = HuxiuItem()
            #item['title'] = sel.xpath('h3/a/text()')[0].extract().encode('utf-8')
            #item['link'] = sel.xpath('h3/a/@href')[0].extract()
            # url = response.urljoin(item['link'])
            #item['desc'] = sel.xpath('div[@class="mob-sub"]/text()')[0].extract().encode('utf-8')
            #print(item['title'],item['link'],item['desc'])

            relativelink = sel.xpath('h3/a/@href')[0].extract()
            url = response.urljoin(relativelink)
            """departing analysis from link getting"""
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        detail = response.xpath('//div[@class="article-wrap"]')
        item = HuxiuItem()
        item['title'] = detail.xpath('h1/text()')[0].extract().encode('utf-8')
        item['link'] = response.url
        item['posttime'] = detail.xpath('div[@class="article-author"]/span[@class="article-time"]/text()')[0].extract()
        item['author'] = detail.xpath('div[@class="article-author"]/span[@class="author-name"]/a/text()')[0].extract().encode('utf-8')
        print(item['title'], item['link'], item['posttime'], item['author'])
        yield item