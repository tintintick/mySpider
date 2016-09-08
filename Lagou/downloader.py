# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class DownLoder(object):
    def getpage(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
            "Connection": "keep-alive"
        }

        request = requests.session().get(url, headers=headers)
        if request.status_code == 200:
            data = request.content
            return data
        else:
            print request.status_code
            return None

    def get_dynamic_page(self, url):

        dcap = DesiredCapabilities.PHANTOMJS
        dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        # dcap["phantomjs.page.settings.resourceTimeout"] = 10
        dcap["phantomjs.page.settings.loadImages"] = False


        try:
            driver = webdriver.PhantomJS(executable_path='./phantomjs',
                                         desired_capabilities=dcap
                                         )

            wait = WebDriverWait(driver, 60)

            time1 = datetime.now()
            # driver.implicitly_wait(3)
            driver.set_page_load_timeout(3)
            driver.get(url)

        except Exception, e:
            # driver.save_screenshot('./t1.png')
            # p = driver.page_source
            # element = wait.until(
            #         EC.presence_of_all_elements_located((By.XPATH, '//div[@class="page-box house-lst-page-box"]/a/@href')))
            # time = datetime.now() - time1
            # print time
            print e.msg

        finally:
            time = datetime.now() - time1
            print time
            driver.save_screenshot('./t.png')
            pagesource = driver.page_source.encode("utf-8")
            driver.close()

        return pagesource


    def get_page_via_post(self, url, pagenum):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
                "Connection": "keep-alive",
                "Reference": "http://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
                "Origin": "http://www.lagou.com",
                "X-Anit-Forge-Code": "0",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Accept": "application/json,text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "X-Anit-Forge-Token": "None"
            }

            data = {
                'first': 'false',
                'pn': pagenum,
                'kd': 'python'
            }

            req = requests.session().post(url, headers=headers, data=data)
            if req.status_code is 200:
                result = req.content

        except Exception, e:
            print e

        return result
