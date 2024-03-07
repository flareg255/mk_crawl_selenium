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

class FourthCrawler(BaseCrawler):
    def fourthCatGet(self):
        pprint.pprint('fourthCatGet start')
        firstCat = self.cateries.getFirstCat(filePath=self.filePath.getFirstCatFilePath())

        for catKey1 in firstCat.keys():
            secondCat = self.cateries.getUnderCat(filePath=self.filePath.getSecondCatFilePath(catName=catKey1))

            httpUrl = self.urls.getBaseUrl()
            catNo = firstCat[catKey1].replace(httpUrl, '')
            for catKey2 in secondCat.keys():
                thirdCat = self.cateries.getUnderCat(filePath=self.filePath.getThirdCatFilePath(catName1=catKey1, catName2=catKey2))
                for catKey3 in thirdCat.keys():
                    self.driver.get(self.urls.getPageUrl(topCat=catNo,underlayerCat=thirdCat[catKey3]))
                    wait = WebDriverWait(self.driver, 10)
                    try:
                        wait.until(EC.presence_of_all_elements_located)
                    except TimeoutException as te:
                        pprint.pprint(te)
                        try:
                            wait.until(EC.presence_of_all_elements_located)
                        except TimeoutException as te2:
                            pprint.pprint(te2)
                        pprint.pprint('fourthCatGet rendering ' + catKey3)

                    time.sleep(2)

                    resultDict = {}
                    dictToDf ={}
                    for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getUnderLinkSelector('4')):
                        if not len(elem.text) == 0 and not elem.text == 'すべて':
                            resultDict[elem.text.strip().replace('\u3000', ' ')] = elem.get_attribute('value')

                    dictToDf = dict(key=list(resultDict.keys()),value=list(resultDict.values()))
                    self.cateries.dictToCsv(dataDict=dictToDf, fileName=self.filePath.getFourthCatFilePath(catName1=catKey1, catName2=catKey2, catName3=catKey3))

        self.driver.quit()

        pprint.pprint('fourthCatGet end')

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
    #     doublequoteAddAry.append('"{0}":""'.format(underlayerCatAry[0]))
    #     doublequoteAddAry.append('"{0}:{1}":""'.format(underlayerCatAry[0], underlayerCatAry[1]))
    #     doublequoteAddAry.append('"{0}:{1}:{2}":""'.format(underlayerCatAry[0], underlayerCatAry[1], underlayerCatAry[2]))
    #     underlayerCatStr =  urllib.parse.quote('{' + ','.join(doublequoteAddAry) + '}')
    #     return self.baseUrl + topCat + '?categories=' + underlayerCatStr