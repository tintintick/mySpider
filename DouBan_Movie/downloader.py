import requests

class DownLoder(object):
    def getpage(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            data = request.text
            return data
        else:
            return None