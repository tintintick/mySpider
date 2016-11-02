import requests
import json
import re

url = "http://vacations.ctrip.com/Package-Booking-Promotion/jsondataprovider/Query"
data = {
		"Data": '{"GroupId":"1","ChannelId":"1","DestinationId":"0","DepartureDate":null,"DepartureCityId":"0","Channel":"1","PageIndex":1,"SaleCity":0}',
		"QType": "queryv3"
	}

header = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36", 
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "en-US,en;q=0.8",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"Origin": "http://vacations.ctrip.com",
		"Referer": "http://vacations.ctrip.com/deals/grouptravel",
		"X-Requested-With": "XMLHttpRequest"
	}

response = requests.post(url, data=data, headers=header)