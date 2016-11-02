# -*- coding:utf-8 -*-
import requests
from lxml import etree
import json


url = 'https://traveln.alitrip.com/temai?spm=181.64014.256151.7.8vK6wv'
header = {':authority': 'traveln.alitrip.com',
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'accept-encoding': 'gzip, deflate, sdch, br',
          'accept-language': 'en-US,en;q=0.8',
          'cache-control': 'max-age=0',
          'referer': 'https://temai.alitrip.com/?spm=181.64014.191938.38.KzEuL1',
          'upgrade-insecure-requests': 1,
          'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36'
}

response = requests.get(url).content
pagetree = etree.HTML(response)
ret = pagetree.xpath('//script')[-2].text[45:-7]
ajson = json.loads(ret)
if ajson['success'] is not True:
    print 'get page error!'
    exit()

products = ajson['items']
item = {}
for product in products:
    if product['dep'] is None:
        item['from'] = 'None'
    else:
        item['from'] = product['dep']

    item['to'] = product['dest']
    item['url'] = product['itemUrl']
    item['picurl'] = product['picUrlTms']
    item['type'] = product['holidayType']
    item['time'] = product['tuanTime']
    item['aprice'] = product['activityPrice']
    item['oprice'] = product['originalPrice']
    item['discount'] = product['saleCount']
    item['description'] = product['shortNameTms']
    # store item into db
    print item
    item.clear()
    exit()