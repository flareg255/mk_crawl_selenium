from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import pandas as pd

import re
import time
import pprint
import urllib.parse

from crawlers.BaseCrawler import BaseCrawler

class ThirdCrawler(BaseCrawler):
    def thirdCatGet(self):
        pprint.pprint('thirdCatGet')
        firstCat = self.cateries.getFirstCat(filePath=self.filePath.getFirstCatFilePath())

        for catKey in firstCat.keys():
            secondCat = self.cateries.getSecondCat(filePath=self.filePath.getSecondCatFilePath(catKey))
            pprint.pprint(secondCat)
            resultDict = {}
            httpUrl = self.urls.getBaseUrl()
            catNo = firstCat[catKey].replace(httpUrl, '')
            for catKey in secondCat.keys():
                self.driver.get(self.getPageUrl(topCat=catNo,underlayerCat=secondCat[catKey]))
                wait = WebDriverWait(self.driver, 10)

                time.sleep(2)

                for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getThirdLinkSelector()):
                    if not len(elem.text) == 0 and not elem.text == 'すべて':
                        resultDict[elem.text.strip()] = elem.get_attribute('value')

                dictionary = dict(key=list(resultDict.keys()),value=list(resultDict.values()))
                self.cateries.dictToCsv(dataDict=dictionary, fileName=self.filePath.getThirdCatFilePath(catKey))

        self.driver.quit()

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

    def getPageUrl(self, topCat, underlayerCat):
        underlayerCatAry = underlayerCat.split(':')
        doublequoteAddAry = []
        doublequoteAddAry.append('"'+ underlayerCatAry[0] + '":' + '""')
        doublequoteAddAry.append('"'+ underlayerCatAry[0] + ':'+ underlayerCatAry[1]+ '":'+ '""' )
        underlayerCatStr =  urllib.parse.quote('{' + ','.join(doublequoteAddAry) + '}')
        return self.baseUrl + topCat + '?categories=' + underlayerCatStr