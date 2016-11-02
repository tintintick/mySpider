# -*- coding:utf-8 -*-

import requests
import json
import time


header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36", 
		  "Accept-Encoding": "gzip, deflate",
		  "Accept-Language": "en-US,en;q=0.8",
		  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
	}

def getCities(header, curdate):
	url= "http://lp.flight.qunar.com/api/qdclowprice?callback=qjson&drange=7&query=search&sort=S1&asc=true&page=1&from=tejia_d_mr&ex_track=&searchType=domestic&per=40&perScrollPage=10&_=abc&ddate="
	qjson = json.loads(requests.get(url+cur_date, headers=header).content[6:-2])['options']['dcity_more']
	cities = []
	for item in qjson:
		for city in item['list']:
			cities.append(city['key']) 

	return cities


def composeURL(host, path, args, city, curdate, page):
	var = "dcity={0}&ddate={1}&page={2}".format(city.encode('utf-8'), curdate, page)
	url = "{0}{1}?{2}&{3}".format(host, path, args, var)
	return url

def getFlightTickets(header, cities, curdate):

	host = "http://lp.flight.qunar.com"
	path = "/api/qdclowprice"
	args = "callback=qjson&drange=7&query=filter&sort=S1&asc=true&from=tejia_d_mr&ex_track=&searchType=domestic&per=40&perScrollPage=10&_=abc"
	page = "1"

	item = {}
	for city in cities:
		# get totoal page number
		url = composeURL(host, path, args, city, curdate, page)
		totalpage = int(json.loads(requests.get(url).content[6:-2])['data']['info']['page'])
		flightnum = int(json.loads(requests.get(url).content[6:-2])['data']['info']['total'])
		
		# get flights
		amount = 0
		for page in range(1, totalpage+1):
			url = composeURL(host, path, args, city, curdate, page)
			flights = json.loads(requests.get(url).content[6:-2])['data']['list']
			for flight in flights:
				item['from'] = flight['dc']
				item['to'] = flight['ac']
				item['price'] = flight['pr']
				item['discount'] = flight['dis']
				item['date'] = flight['dd']
				item['time'] = flight['dt']
				print item
				# store it into mongodb
				# store item then clear
				# item.clear()
				amount = amount + 1
		if amount is not flightnum:
			print "{0} flight number is error, amount is {1}".format(city, amount)
			exit()

		exit()




cur_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
cities = getCities(header, cur_date)
getFlightTickets(header, cities, cur_date)



