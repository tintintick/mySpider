# -*- coding:utf-8 -*-
import requests
import json
from lxml import etree
import base64
import re

# g_constant = 0


def get_all_cities():
    url = 'http://www.tuniu.com/flight/international/getCities'
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    tjson = json.loads(requests.get(url, headers=header).content)
    return tjson['data']


def get_city_code(dept_city_name, arr_city_name):
    dept_city_code = ''
    arr_city_code = ''
    cities = get_all_cities()
    for city in cities:
        if city['cityName'] == dept_city_name.decode('utf-8'):
            dept_city_code = base64.encodestring(str(city['cityCode']))
        if city['cityName'] == arr_city_name.decode('utf-8'):
            arr_city_code = base64.encodestring(str(city['cityCode']))
        if dept_city_code != '' and arr_city_code != '':
            break

    return dept_city_code.strip('\n'), arr_city_code.strip('\n')


def extract_product_info(pagetree, response):
    count = 0

    errnames = re.findall(u'><[-0-9\u4e00-\u9fa5]+><', response.decode('utf-8'))
    item = {}
  
    products = pagetree.xpath('//*[@id="fortop"]/div/div[3]/div[2]/div[2]/ul/li')
    for product in products:
        item['discount'] = product.xpath('./a[@class="line_img"]/div[@class="discount2"]/span/text()')[0]
  
        mask = product.xpath('./a[@class="line_img"]/div[@class="mask"]/span')
        item["deptCity"] = mask[0].text
        item["type"] = mask[1].text
        item["time"] = mask[2].text
  
        info = product.xpath('./a[@class="line_info"]')[0]
        try:
            item['name'] = info.xpath('./p[@class="name"]/text()')[0]
        except:
            item['name'] = errnames.pop(0)[2:-2]

        item['pprice'] = info.xpath('./div[@class="line_price"]/span/span/text()')[0]
        item['oprice'] = info.xpath('./div/span[2]/text()')[0]
        item['url'] = info.xpath('./div[@class="line_price"]/p/@href')[0]
        try:
            item['highlight'] = info.xpath('./p[@class="highlights2"]/text()')[0]
        except:
            #print item['url']
            item['highlight'] = ''

        item.clear()
        count = count + 1
        print count


def extract_product_city_list(dept_city_name, url, header):
    
    response = requests.get(url, headers=header).content
    pagetree = etree.HTML(response)

    dept_list = pagetree.xpath('//div[@class="city_list hide"]')[0]
    dept_cities = dept_list.xpath('./div[2]/ul/li/div/a/text()')
    dept_urls = dept_list.xpath('./div[2]/ul/li/div/a/@href')

    arr_list = pagetree.xpath('//div[@class="city_list hide"]')[1]
    arr_cities = arr_list.xpath('./div[2]/ul/li/div/a/text()')
    arr_urls = arr_list.xpath('./div[2]/ul/li/div/a/@href')

    dept_dict = dict(zip(dept_cities, dept_urls))
    arr_dict = dict(zip(dept_cities, dept_urls))

    if dept_city_name.decode('utf-8') not in dept_dict.keys():
        return {}, {}

    return dept_dict, arr_dict



def get_products(dept_city_name, arr_city_name, url, header):

    dept_dict, arr_dict = extract_product_city_list(dept_city_name, url, header)
    if dept_dict == {} and arr_dict == {}:
        print "no dept city product"
        return None

    # get products
    product_url = 'http://temai.tuniu.com' + dept_dict[dept_city_name.decode('utf-8')]
    response = requests.get(product_url, headers=header).content
    pagetree = etree.HTML(response)
    extract_product_info(pagetree, response)
    try:
        pagesum = int(pagetree.xpath('//span[@class="page_sum"]/text()')[0][1])
        for num in range(2, pagesum + 1):
            cururl = product_url + 'p' + str(num)
            print cururl
            response = requests.get(cururl, headers=header).content
            pagetree = etree.HTML(response)
            extract_product_info(pagetree, response)
    except:
        print "only one page"


def extract_liner_info(pagetree, response):
    count = 0

    errnames = re.findall(u'><[-0-9\u4e00-\u9fa5]+><', response.decode('utf-8'))
    item = {}
  
    products = pagetree.xpath('//*[@id="fortop"]/div/div[3]/div[2]/div[2]/ul/li')
    for product in products:
        item['discount'] = product.xpath('./a[@class="line_img"]/div[@class="discount2"]/span/text()')[0]
  
        mask = product.xpath('./a[@class="line_img"]/div[@class="mask"]/span')
        item["deptCity"] = mask[0].text
        item["type"] = '邮轮'
        item["time"] = mask[1].text
  
        info = product.xpath('./a[@class="line_info"]')[0]
        try:
            item['name'] = info.xpath('./p[@class="name"]/text()')[0]
        except:
            item['name'] = errnames.pop(0)[2:-2]

        item['pprice'] = info.xpath('./div[@class="line_price"]/span/span/text()')[0]
        item['oprice'] = info.xpath('./div/span[2]/text()')[0]
        item['url'] = info.xpath('./div[@class="line_price"]/p/@href')[0]
        try:
            item['highlight'] = info.xpath('./p[@class="highlights2"]/text()')[0]
        except:
            #print item['url']
            item['highlight'] = ''

        item.clear()
        count = count + 1
        print count
def get_liner_products(url, header):
    
    # get products
    response = requests.get(url, headers=header).content
    pagetree = etree.HTML(response)
    extract_liner_info(pagetree, response)
    try:
        pagesum = int(pagetree.xpath('//span[@class="page_sum"]/text()')[0][1])
        for num in range(2, pagesum + 1):
            cururl = product_url + 'p' + str(num)
            print cururl
            response = requests.get(cururl, headers=header).content
            pagetree = etree.HTML(response)
            extract_liner_info(pagetree, response)
    except:
        print "only one page"


dept_city_name='成都'
arr_city_name='北京'
dept_city_code, arr_city_code = get_city_code(dept_city_name='成都', arr_city_name='北京')


header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'Cookie': 'tuniu_partner=MTAwLDAsLDI2OWJhMjJhNDAxOWQyNDRjYzNkMGU4ODZkMjQ1NGFk; p_phone_400=4007-999-999; OLBSESSID=797c7t0vrebf8dpgtr2cjg6197; _tacau=MCw1YmY4M2ZlYi1lY2QyLTQ3MGItZWE5NC00MjA1ZjM1MDhkN2Us; _tacz2=taccsr%3D%28direct%29%7Ctacccn%3D%28none%29%7Ctaccmd%3D%28none%29%7Ctaccct%3D%28none%29%7Ctaccrt%3D%28none%29; _taca=1477533277619.1477533277619.1477533277619.1; _tacc=1; PageSwitch=1%2C213612736; __xsptplusUT_352=1; MOBILE_APP_SETTING_OPEN-124=1; MOBILE_APP_SETTING_STATE-124=CLOSE; _pzfxuvpc=1477533277671%7C8609357373767715853%7C3%7C1477533290475%7C1%7C%7C1174412762213237200; _pzfxsvpc=1174412762213237200%7C1477533277671%7C3%7C; _tact=N2NlMWE2OTctZjdjYi02NWZkLWRlN2YtNDNmZjI2OGYwZGM3; _tacb=MjU0ZWM0ZGQtNDkzZC0zOTA3LTIyMDItNjNhNGU5ZmQwNTli; __xsptplus352=352.1.1477533281.1477533292.4%234%7C%7C%7C%7C%7C%23%23gRi5UZx0kl22-Dh4Cqk_Ka4_dD7yPq7E%23; Hm_lvt_51d49a7cda10d5dd86537755f081cc02=1477533278; Hm_lpvt_51d49a7cda10d5dd86537755f081cc02=1477533292; __utma=1.1986001297.1477533278.1477533278.1477533278.1; __utmb=1.4.9.1477533278; __utmc=1; __utmz=1.1477533278.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); tuniuuser_citycode='
}
header['Cookie'] = header['Cookie'] + dept_city_code

domestic_url = 'http://temai.tuniu.com/domestic/'
abroad_url = 'http://temai.tuniu.com/abroad/'
liner_url = 'http://temai.tuniu.com/youlun/'

get_products(dept_city_name, arr_city_name, domestic_url, header)
get_products(dept_city_name, arr_city_name, abroad_url, header)
get_liner_products(liner_url, header)