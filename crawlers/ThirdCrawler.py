from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import pprint

from crawlers.BaseCrawler import BaseCrawler

class ThirdCrawler(BaseCrawler):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def thirdCatGet(self):
        pprint.pprint('thirdCatGet start')
        firstCat = self.catergories.getFirstCat(filePath=self.filePath.getCatFilePath(catName='first_cat', layerList=['first_cat']))

        for catKey1 in firstCat.keys():
            # secondCat = self.catergories.getUnderCat(filePath=self.filePath.getSecondCatFilePath(catName=catKey1))
            secondCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='second_cat', layerList=[catKey1]))
            # httpUrl = self.urls.getBaseUrl()
            # catNo = firstCat[catKey1].replace(httpUrl, '')

            catNo = self.getCatNo(firstCat[catKey1])

            for catKey2 in secondCat.keys():
                self.catDataToCsv(url=self.urls.getPageUrl(topCat=catNo,underlayerCat=secondCat[catKey2]), catKey=catKey2, execFunction='third_cat', layers=[catKey1], underLinkSelector='3')

        pprint.pprint('thirdCatGet end')