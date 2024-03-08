from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import re
import time
import pprint

from crawlers.BaseCrawler import BaseCrawler

class ItemsCrawler(BaseCrawler):
    pageCnt = 1

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.pageCnt = 1

    def itemsGet(self):
        pprint.pprint('itemsGet start')
        firstCat = self.cateries.getFirstCat(filePath=self.filePath.getFirstCatFilePath())

        for catKey in firstCat.keys():
            self.recursivePageItemget(url=firstCat[catKey], catKey=catKey)

        pprint.pprint('itemsGet start')

    def recursivePageItemget(self, url, catKey):
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)

        try:
            wait.until(EC.presence_of_all_elements_located)
        except TimeoutException as te:
            pprint.pprint(te)
            try:
                wait.until(EC.presence_of_all_elements_located)
            except TimeoutException as te2:
                pprint.pprint(te2)

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
        time.sleep(20)

        httpUrl = self.urls.getRemoveUrlString()
        rtSidRe = self.urls.getRemoveQueryRe()

        resultDict = {}
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector()):
            resultDict[re.sub(rtSidRe, '',elem.get_attribute('href').replace(httpUrl, ''))] = elem.get_attribute('title')

        dictionary = dict(key=list(resultDict.keys()),value=list(resultDict.values()))
        pprint.pprint(resultDict)
        pprint.pprint(dictionary)
        self.cateries.dictToCsv(dataDict=dictionary, fileName=self.filePath.getItemFilePath())

        endFlag = False
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getNextPageBtnSelector()):
            if elem.get_attribute('class') in self.cssSelectors.btnDisableSelector():
                endFlag = True
            pprint.pprint(elem.get_attribute('class'))

        if endFlag:
            return
        else:
            self.pageCnt += 1
            itemNumber = 60 * self.pageCnt
            self.urls.getRecursivePageUrl(url=url, param1=self.pageCnt, param2=itemNumber)
            return
            # self.recursivePageItemget(url=firstCat[catKey], catKey=catKey)