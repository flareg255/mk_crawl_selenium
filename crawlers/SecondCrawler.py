import pprint

from crawlers.BaseCrawler import BaseCrawler

class SecondCrawler(BaseCrawler):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def secondCatGet(self):
        pprint.pprint('secondCatGet start')

        firstCat = self.catergories.getFirstCat(filePath=self.filePath.getCatFilePath(catName='first_cat', layerList=['first_cat']))

        for catKey in firstCat.keys():
            self.catDataToCsv(url=firstCat[catKey], catKey=catKey, execFunction='second_cat', layers=[], underLinkSelector='2')

        pprint.pprint('secondCatGet end')