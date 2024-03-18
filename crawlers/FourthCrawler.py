from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import pprint

from crawlers.BaseCrawler import BaseCrawler

class FourthCrawler(BaseCrawler):
    start = 'fourthCatGet start'
    rendering = 'fourthCatGet rendering'
    exceptionStart = 'fourthCatGet exception----------------------------------------'
    end = 'fourthCatGet end'

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def fourthCatGet(self):
        self.fileWRService.logOutPut(self.start, self.filePath.getLogFilePath())
        pprint.pprint(self.start)
        firstCat = self.catergories.getFirstCat(filePath=self.filePath.getCatFilePath(catName='first_cat', layerList=['first_cat']))

        for catKey1 in firstCat.keys():
            secondCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='second_cat', layerList=[catKey1]))
            catNo = self.getCatNo(firstCat[catKey1])

            for catKey2 in secondCat.keys():
                thirdCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='third_cat', layerList=[catKey1, catKey2]))
                for catKey3 in thirdCat.keys():
                    try:
                        self.catDataToCsv(url=self.urls.getPageUrl(topCat=catNo,underlayerCat=thirdCat[catKey3]), catKey=catKey3, execFunction='fourth_cat', layers=[catKey1, catKey2], underLinkSelector='4')
                    except Exception as e:
                        self.fileWRService.logOutPut(str(e), self.filePath.getLogFilePath())
                        pprint.pprint(self.exceptionStart)
                        pprint.pprint(str(e))
                        self.fileWRService.flagOutPut('3', self.filePath.getFlagFilePath())
                        return

        self.fileWRService.flagOutPut('4', self.filePath.getFlagFilePath())
        self.fileWRService.logOutPut(self.end, self.filePath.getLogFilePath())
        pprint.pprint(self.end)