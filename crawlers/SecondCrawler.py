from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


import pandas as pd

import re
import time
import pprint
import urllib.parse

from crawlers.BaseCrawler import BaseCrawler

class SecondCrawler(BaseCrawler):
    def secondCatGet(self):
        pprint.pprint('secondCatGet start')

        firstCat = self.cateries.getFirstCat(filePath=self.filePath.getFirstCatFilePath())

        for catKey in firstCat.keys():
            self.driver.get(firstCat[catKey])
            wait = WebDriverWait(self.driver, 10)
            try:
                wait.until(EC.presence_of_all_elements_located)
            except TimeoutException as te:
                pprint.pprint(te)
                try:
                    wait.until(EC.presence_of_all_elements_located)
                except TimeoutException as te2:
                    pprint.pprint(te2)

            pprint.pprint('secondCatGet rendering ' + catKey)

            time.sleep(2)

            secoundDict = {}
            for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getUnderLinkSelector('2')):
                if not len(elem.text) == 0 and not elem.text == 'すべて':
                    secoundDict[elem.text.strip().replace('\u3000', ' ')] = elem.get_attribute('value')

            dictionary = dict(key=list(secoundDict.keys()),value=list(secoundDict.values()))
            self.cateries.dictToCsv(dataDict=dictionary, fileName=self.filePath.getSecondCatFilePath(catName=catKey))

        self.driver.quit()

        pprint.pprint('secondCatGet end')

    def itemsGet(self):
        self.driver.get(self.firstUrl)
        wait = WebDriverWait(self.driver, 10)

        javascript = 'var cnt = 0;\
        var scrollVal = 0;\
        function scroll() {\
            window.scrollTo(0, document.body.scrollHeight);\
            cnt++;\
            if (cnt == 4) {\
                return;\
            }\
            setTimeout(scroll, 5000);\
        }\
        scroll();'

        self.driver.execute_script(javascript)
        time.sleep(30)

        httpUrl = self.urls.getRemoveUrlString()
        rtSidRe = re.compile(self.urls.getRemoveQueryRe())

        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector()):
            pprint.pprint(elem.get_attribute('title'))
            pprint.pprint(re.sub(rtSidRe, '',elem.get_attribute('href').replace(httpUrl, '')))

        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getNextPageBtnSelector()):
            pprint.pprint(elem.get_attribute('class'))

        self.driver.quit()

    # def getPageUrl(self, topCat, underlayerCat):
    #     underlayerCatAry = underlayerCat.split(':')
    #     doublequoteAddAry = []
    #     doublequoteAddAry.append('"'+ underlayerCatAry[0] + '":' + '""')
    #     doublequoteAddAry.append('"'+ underlayerCatAry[0] + ':'+ underlayerCatAry[1]+ '":'+ '""' )
    #     underlayerCatStr =  urllib.parse.quote('{' + ','.join(doublequoteAddAry) + '}')
    #     return self.baseUrl + topCat + '?categories=' + underlayerCatStr