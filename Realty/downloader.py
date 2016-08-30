import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class DownLoder(object):
    def getpage(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            data = request.text
            return data
        else:
            return None

    def dongtai(self):

        dcap = DesiredCapabilities.PHANTOMJS
        dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        # dcap["phantomjs.page.settings.resourceTimeout"] = 10
        dcap["phantomjs.page.settings.loadImages"] = False

        driver = webdriver.PhantomJS(executable_path='./phantomjs',
                                     desired_capabilities=dcap
                                     )
        time1 = datetime.now()
        # driver.implicitly_wait(0.5)
        driver.get('http://bj.lianjia.com/chengjiao/chaoyang/')
        time = datetime.now() - time1

        try:
            # driver.save_screenshot('./test.png')
            elements = driver.find_elements_by_xpath(u"//ul[@class='listContent']/li/div[@class='info']")
            titles = []
            for element in elements:
                titleElement = element.find_element_by_xpath(u"div[@class='title']/a")
                titles.append(titleElement.text)
        except Exception, e:
            print e
        finally:
            driver.close()

            # try:
            #     element = WebDriverWait(driver, 5).until(
            #         EC.presence_of_element_located((By.XPATH, u"//ul[@class='listContent']/li/div[@class='info']"))
            #     )
            #     time = datetime.now()-time1
            #     print time
            #
            # except Exception, e:
            #     print e
            #
            # finally:
            #     driver.quit()