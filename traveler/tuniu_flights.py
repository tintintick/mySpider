# -*- coding:utf-8 -*-
import requests
import json
import base64
from urllib import urlencode
from operator import itemgetter


def getCities():
	url = 'http://www.tuniu.com/flight/international/getCities'
	header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
	tjson = json.loads(requests.get(url, headers=header).content)
	return  tjson['data']


def getCheapFlights(cities):
	url = 'http://flight-api.tuniu.com/query/queryCheapTickets?callback=tjson'
	header = {'Connection': 'keep-alive',
			  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
			  'Accept': '*/*',
			  'Referer': 'http://www.tuniu.com/flight/',
			  'Accept-Encoding': 'gzip, deflate, sdch, br',
			  'Cookie': 'tuniu_partner=MTAwLDAsLDI2OWJhMjJhNDAxOWQyNDRjYzNkMGU4ODZkMjQ1NGFk; p_phone_400=4007-999-999; OLBSESSID=797c7t0vrebf8dpgtr2cjg6197; _tacau=MCw1YmY4M2ZlYi1lY2QyLTQ3MGItZWE5NC00MjA1ZjM1MDhkN2Us; _tacz2=taccsr%3D%28direct%29%7Ctacccn%3D%28none%29%7Ctaccmd%3D%28none%29%7Ctaccct%3D%28none%29%7Ctaccrt%3D%28none%29; _taca=1477533277619.1477533277619.1477533277619.1; _tacc=1; PageSwitch=1%2C213612736; __xsptplusUT_352=1; MOBILE_APP_SETTING_OPEN-124=1; MOBILE_APP_SETTING_STATE-124=CLOSE; _pzfxuvpc=1477533277671%7C8609357373767715853%7C3%7C1477533290475%7C1%7C%7C1174412762213237200; _pzfxsvpc=1174412762213237200%7C1477533277671%7C3%7C; _tact=N2NlMWE2OTctZjdjYi02NWZkLWRlN2YtNDNmZjI2OGYwZGM3; _tacb=MjU0ZWM0ZGQtNDkzZC0zOTA3LTIyMDItNjNhNGU5ZmQwNTli; __xsptplus352=352.1.1477533281.1477533292.4%234%7C%7C%7C%7C%7C%23%23gRi5UZx0kl22-Dh4Cqk_Ka4_dD7yPq7E%23; Hm_lvt_51d49a7cda10d5dd86537755f081cc02=1477533278; Hm_lpvt_51d49a7cda10d5dd86537755f081cc02=1477533292; __utma=1.1986001297.1477533278.1477533278.1477533278.1; __utmb=1.4.9.1477533278; __utmc=1; __utmz=1.1477533278.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); tuniuuser_citycode='
	}

	for city in cities:
		citycode = base64.encodestring(str(city['cityCode'])).strip('\n')
		# citycode = base64.encodestring('1740152').strip('\n')
		header['Cookie'] = header['Cookie'] + citycode
		tjson = json.loads(requests.get(url, headers=header).content[6:-1])
		
		if  int(tjson['data']['beginCityCode']) == city['cityCode']:
			flightInfo = tjson['data']['cityFlightInfo']
			airComFlightInfo = tjson['data']['airComFlightInfo']
			for key in airComFlightInfo.keys():
				airComRoundTrip = airComFlightInfo[key]['roundTrip']
				for x in airComRoundTrip:
					print x
				airComSingleTrip = airComFlightInfo[key]['singleTrip']
			exit()
				
			# roundTrip
			# roundTrips = flightinfo['roundTrip']
			# singleTrip
			# singleTrips = flightinfo['singleTrip']

cities = getCities()
#sorted_by_code = sorted(cities, key=itemgetter('cityCode'))
#for x in sorted_by_code:
#	print str(x['cityCode']) + '/' + x['cityName']
getCheapFlights(cities)