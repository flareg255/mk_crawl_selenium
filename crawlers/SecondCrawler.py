
from selenium.webdriver.common.by import By


import time
import pprint

from crawlers.BaseCrawler import BaseCrawler

class SecondCrawler(BaseCrawler):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def secondCatGet(self):
        pprint.pprint('secondCatGet start')

        firstCat = self.cateries.getFirstCat(filePath=self.filePath.getFirstCatFilePath())

        for catKey in firstCat.keys():
            self.catDataToCsv(url=firstCat[catKey], catKey=catKey, execFunction='second_cat_', layers=[], underLinkSelector='2')

        pprint.pprint('secondCatGet end')