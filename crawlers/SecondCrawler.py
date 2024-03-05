from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import pandas as pd

import re
import time
import pprint

from crawlers.BaseCrawler import BaseCrawler

class SecondCrawler(BaseCrawler):
    def secondCatGet(self):
        self.driver.get(self.firstUrl)
        wait = WebDriverWait(self.driver, 10)

        time.sleep(2)

        selectDict = {}
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectorGet.getSecondLinkSelector()):
            if not len(elem.text) == 0 and not elem.text == 'すべて':
                selectDict[elem.text.strip()] = elem.get_attribute('value')

        dictionary = dict(key=list(selectDict.keys()),value=list(selectDict.values()))

        df=pd.DataFrame(dictionary)
        df.to_csv('./data/select_cat.csv', header=False, index=False, encoding='cp932')

        pprint.pprint(df)
        self.driver.quit()

    def itemsGet(self):
        self.driver.get(self.firstUrl)
        wait = WebDriverWait(self.driver, 10)

        javascript = 'var cnt = 0;\
        var scrollVal = 0;\
        function scroll() {\
            console.log(window.innerHeight);\
            window.scrollTo(0, document.body.scrollHeight);\
            cnt++;\
            console.log(window.innerHeight);\
            if (cnt == 4) {\
                return;\
            }\
            setTimeout(scroll, 10000);\
        }\
        scroll();'

        self.driver.execute_script(javascript)
        time.sleep(10)

        selectDict = {}
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectorGet.getSecondLinkSelector()):
            if not len(elem.text) == 0 and not elem.text == 'すべて':
                selectDict[elem.text.strip()] = elem.get_attribute('value')

        httpUrl = self.urlGet.getRemoveUrlString()
        rtSidRe = re.compile(self.urlGet.getRemoveQueryRe())

        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectorGet.getItemsWrapSelector()):
            pprint.pprint(elem.get_attribute('title'))
            pprint.pprint(re.sub(rtSidRe, '',elem.get_attribute('href').replace(httpUrl, '')))

        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectorGet.getNextPageBtnSelector()):
            pprint.pprint(elem.get_attribute('class'))

        dictionary = dict(key=list(selectDict.keys()),value=list(selectDict.values()))

        df=pd.DataFrame(dictionary)
        df.to_csv('./data/select_cat.csv', header=False, index=False, encoding='cp932')

        pprint.pprint(df)
        self.driver.quit()

    def getItemPageUrl(self, topCat, underlayerCat, pageNo,):
        return self.baseUrl + topCat + underlayerCat + pageNo