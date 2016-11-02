# -*- coding:utf-8 -*-
import requests
import json
from urllib import quote



#def searchFlight(depCity, depCityName, arrCity, arrCityName, depDate):
def searchFlight(depCityName, arrCityName, depDate):
    page = 'https://trip.taobao.com/jipiao/'
    s = requests.session()
    s.get(page)

    host = 'https://sjipiao.alitrip.com'
    path = '/searchow/search.htm'
    items = {'callback': 'ajson',
             'tripType': '0',
             #'depCity': depCity,
             'depCityName': quote(depCityName),
             #'arrCity': arrCity,
             'arrCityName': quote(arrCityName),
             'depDate': depDate,
             'searchSource': '99',
             'searchBy': '1280',
             'needMemberPrice': 'true',
             '_input_charset': 'utf-8'
             }

    args = ''
    for key in items:
        args += key + '=' + items[key] + '&'

    args = args[:-1]

    url = '{0}{1}?{2}'.format(host, path, args)
    header = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'accept-encoding': 'gzip, deflate, sdch, br',
              'accept-language': 'en-US,en;q=0.8',
              'cache-control': 'max-age=0',
              'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
              'upgrade - insecure - requests': '1',
              'cookie': 'cna=fI+YEH7Dw10CAW64BNuRKi6Q; cookie2=1c77fdca0ddc3c4acde5014f4de58f97; t=b19a8c4d17f59c005cb99905735de97e; _tb_token_=A2MesRfzlWjK; CNZZDATA30066717=cnzz_eid%3D258578843-1477547258-https%253A%252F%252Fwww.alitrip.com%252F%26ntime%3D1477547258; l=AvX1qnEuxWcpwN/LogT5jY9hhXuvi6mM; isg=Ap2dqAyhmS3vAX0Bbv6faRfIrHCArtEMeS1wLl9iIvQrFr1IJwrh3GuEJr3q'
              }

    ret = requests.get(url, headers=header).content.decode('gbk').encode('utf-8')
    startpos = ret.index('{')
    ajson = json.loads(ret[startpos:-3])
    
    return ajson

def dataExtract(ajson):
    aircodeNameMap = ajson['aircodeNameMap']
    airportMap = ajson['airportMap']
    flights = ajson['flight']
    arrCity = ajson['arrCityName']
    depCity = ajson['depCityName']
    flightType = ajson['flightTypeMap']


    item = {}
    for flight in flights:
        pass



ajson = searchFlight('上海', '北京', '2017-10-01')
#dataExtract(ajson)