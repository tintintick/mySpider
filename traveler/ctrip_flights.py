# -*- coding:utf-8 -*-

import requests
import json
import re


def getCities():
    url = "http://webresource.c-ctrip.com/code/cquery/resource/address/flight/fuzzy_start_poi_timezone_gb2312.js??CR_2016_04_26_00_00_00"
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://vacations.ctrip.com",
        "Referer": "http://vacations.ctrip.com/deals/grouptravel",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.get(url, headers=header).content[56:-1].decode('gb2312')
    ret = re.sub('\"', '\'', response)
    ret = re.sub('display', '\'display\'', ret)
    ret = re.sub('data', '\'data\'', ret)
    ret = eval(ret)

    cities = []

    for alpha in 'ABCDEF':
        for city in ret['ABCDEF'][alpha]:
            city = city['data'].split('|')[1].split('(')
            cities.append({'name': city[0], 'code': city[1][:-1]})

    for alpha in 'GHIJ':
        if alpha is not 'I':
            for city in ret['GHIJ'][alpha]:
                city = city['data'].split('|')[1].split('(')
                cities.append({'name': city[0], 'code': city[1][:-1]})

    for alpha in 'KLMN':
        for city in ret['KLMN'][alpha]:
            city = city['data'].split('|')[1].split('(')
            cities.append({'name': city[0], 'code': city[1][:-1]})

    for alpha in 'PQRSTUVW':
        if alpha is not 'U' and alpha is not 'V':
            for city in ret['PQRSTUVW'][alpha]:
                city = city['data'].split('|')[1].split('(')
                cities.append({'name': city[0], 'code': city[1][:-1]})

    for alpha in 'XYZ':
        for city in ret['XYZ'][alpha]:
            city = city['data'].split('|')[1].split('(')
            cities.append({'name': city[0], 'code': city[1][:-1]})

    return cities


def getInfo(flights, city):
    item = {}
    for flight in flights:
        item['from'] = city['name']
        item['to'] = flight['aCityName']
        item['ddate'] = flight['flightDetail']['departDateString']
        item['dweekday'] = flight['flightDetail']['departWeekday']
        item['dflightno'] = flight['flightDetail']['departFlightNo']
        item['rdate'] = flight['flightDetail']['returnDateString']
        item['rweekday'] = flight['flightDetail']['returnWeekday']
        item['rflightno'] = flight['flightDetail']['returnFlightNo']
        item['duration'] = flight['flightDetail']['duration']
        item['price'] = flight['totalNetPrice']
        item['discount'] = flight['discountRate']
        # store item into db
        print item
        item.clear()


def getTickets(cities):
    temp = {"inputDepartureCity": "", "inputDepartureCityName": "", "travelType": "", "departStringDate": "任何时间",
            "departDateRanges": [], "inputArrivalCities": {"themes": [], "cities": [], "areas": []},
            "inputArrivalCitiesMap": {"themes": [], "cities": [], "areas": [], "filter": {}},
            "sortingType": "PRICE_ASC", 'inputDepartureCity': '', 'inputDepartureCityName': '',
            'travelType': ''}

    # post city search data
    for city in cities:
        url = 'http://flights.ctrip.com/fuzzy/search'
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.7.1',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json; charset=utf-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://flights.ctrip.com/fuzzy/',
        }


        temp['inputDepartureCity'] = city['code']
        temp['inputDepartureCityName'] = city['name']

        # ONEWAY
        travelType = 'ONEWAY'
        temp['travelType'] = travelType
        data = json.dumps(temp)[:-1] + ' ,"isSearchPage":true, "isIncludedTax":true' + '}'
        ret = json.loads(requests.post(url, data=data, headers=header).content)['fuzzyFlightList']
        if len(ret) is not 0:
            flights = ret[0]['flightResultList']
            getInfo(flights, city)
            print 'OK'

        # ROUNDTRIP
        # travelType = 'ROUNDTRIP'
        # temp['travelType'] = travelType
        # data = json.dumps(temp)[:-1] + ' ,"isSearchPage":true, "isIncludedTax":true' + '}'
        # ret = json.loads(requests.post(url, data=data, headers=header).content)['fuzzyFlightList']
        # if len(ret) is not 0:
        #     flights = ret[0]['flightResultList']
        #     getInfo(flights, city)
        #     print 'OK'


cities = getCities()
getTickets(cities)
