import requests
import os
import json


host = "https://zt.dujia.qunar.com"
path = "/tejia/tejia_get_list.php"
args = "callback=qjson&displaynum=15&page" # args0 = "callback=jQuery17206198033042905551_1477012775316&from=tejiaindex01&displaynum=15&_=1477013982495&page"
pagenum = "1"
# print 

def crawl(host, path, args, pagenum):
	header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"}
	url = "{0}{1}?{2}={3}".format(host,path,args,pagenum)
	response = requests.get(url, headers = header)
	ret = response.content[6:-1]
	return json.loads(ret)

qjson = crawl(host, path, args, pagenum)

total = qjson['AllTeamNum']
allpage = qjson['AllPageNum']

for i in range(1, allpage+1):
	result = crawl(host, path, args, i)
	if qjson['ret'] == 1:
		headData = result['headData']
		print i
'''		for item in headData:
			print item['days']
			print item['dest']
			print item['leftday']
			print item['linkurl']
			print item['price']
			print item['pdContain']
			print item['rate']
			print item['startDate']
			print item['type']
'''