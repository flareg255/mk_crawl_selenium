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
        firstCat = self.catergories.getFirstCat(filePath=self.filePath.getCatFilePath(catName='first_cat', layerList=['first_cat']))

        for catKey1 in firstCat.keys():
            secondCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='second_cat', layerList=[catKey1]))

            # httpUrl = self.urls.getBaseUrl()
            # catNo = firstCat[catKey1].replace(httpUrl, '')

            catNo = self.getCatNo(firstCat[catKey1])

            for catKey2 in secondCat.keys():
                # thirdCat = self.catergories.getUnderCat(filePath=self.filePath.getThirdCatFilePath(catName1=catKey1, catName2=catKey2))
                thirdCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='second_cat', layerList=[catKey1, catKey2]))
                for catKey3 in thirdCat.keys():
                    fourthCat = self.catergories.getUnderCat(filePath=self.filePath.getFourthCatFilePath(catName1=catKey1, catName2=catKey2, catName3=catKey3))
                    for catKey4 in fourthCat.keys():
                        self.catDataToCsv(url=self.urls.getPageUrl(topCat=catNo,underlayerCat=thirdCat[catKey4]), catKey=catKey4, execFunction='fifth_cat', layers=[catKey1, catKey2, catKey3], underLinkSelector='5')

        pprint.pprint('fifthCatGet end')