from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import pprint

from crawlers.BaseCrawler import BaseCrawler

class FourthCrawler(BaseCrawler):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

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
                    self.catDataToCsv(url=self.urls.getPageUrl(topCat=catNo,underlayerCat=thirdCat[catKey3]), catKey=catKey3, execFunction='fourth_cat_', layers=[catKey1, catKey2], underLinkSelector='4')

        pprint.pprint('fourthCatGet end')