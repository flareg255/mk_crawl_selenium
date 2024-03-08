from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import pprint

from crawlers.BaseCrawler import BaseCrawler

class FifthCrawler(BaseCrawler):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def fifthCatGet(self):
        pprint.pprint('fifthCatGet start')
        firstCat = self.cateries.getFirstCat(filePath=self.filePath.getFirstCatFilePath())

        for catKey1 in firstCat.keys():
            secondCat = self.cateries.getUnderCat(filePath=self.filePath.getSecondCatFilePath(catName=catKey1))

            httpUrl = self.urls.getBaseUrl()
            catNo = firstCat[catKey1].replace(httpUrl, '')
            for catKey2 in secondCat.keys():
                thirdCat = self.cateries.getUnderCat(filePath=self.filePath.getThirdCatFilePath(catName1=catKey1, catName2=catKey2))
                for catKey3 in thirdCat.keys():
                    fourthCat = self.cateries.getUnderCat(filePath=self.filePath.getFourthCatFilePath(catName1=catKey1, catName2=catKey2, catName3=catKey3))
                    for catKey4 in fourthCat.keys():
                        self.catDataToCsv(url=self.urls.getPageUrl(topCat=catNo,underlayerCat=thirdCat[catKey4]), catKey=catKey4, execFunction='fifth_cat_', layers=[catKey1, catKey2, catKey3], underLinkSelector='5')
        #                 self.driver.get(self.urls.getPageUrl(topCat=catNo,underlayerCat=fourthCat[catKey4]))
        #                 wait = WebDriverWait(self.driver, 10)
        #                 try:
        #                     wait.until(EC.presence_of_all_elements_located)
        #                 except TimeoutException as te:
        #                     pprint.pprint(te)
        #                     try:
        #                         wait.until(EC.presence_of_all_elements_located)
        #                     except TimeoutException as te2:
        #                         pprint.pprint(te2)
        #                     pprint.pprint('fourthCatGet rendering ' + catKey3)

        #                 time.sleep(2)

        #                 resultDict = {}
        #                 dictToDf ={}
        #                 if not len(self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getUnderLinkSelector('5'))) == 0:
        #                     for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getUnderLinkSelector('5')):
        #                         if not len(elem.text) == 0 and not elem.text == 'すべて':
        #                             resultDict[elem.text.strip().replace('\u3000', ' ')] = elem.get_attribute('value')

        #                     dictToDf = dict(key=list(resultDict.keys()),value=list(resultDict.values()))
        #                     self.cateries.dictToCsv(dataDict=dictToDf, fileName=self.filePath.getFifththCatFilePath(catName1=catKey1, catName2=catKey2, catName3=catKey3, catName4=catKey4))

        # self.driver.quit()

        pprint.pprint('fifthCatGet end')