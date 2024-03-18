import pprint

from crawlers.BaseCrawler import BaseCrawler

class SecondCrawler(BaseCrawler):
    start = 'secondCatGet start'
    rendering = 'secondCatGet rendering'
    exceptionStart = 'secondCatGet exception----------------------------------------'
    end = 'secondCatGet end'

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def secondCatGet(self):
        self.fileWRService.logOutPut(self.start, self.filePath.getLogFilePath())
        pprint.pprint(self.start)

        firstCat = self.catergories.getFirstCat(filePath=self.filePath.getCatFilePath(catName='first_cat', layerList=['first_cat']))

        for catKey in firstCat.keys():
            try:
                self.catDataToCsv(url=firstCat[catKey], catKey=catKey, execFunction='second_cat', layers=[], underLinkSelector='2')
            except Exception as e:
                self.fileWRService.logOutPut(str(e), self.filePath.getLogFilePath())
                pprint.pprint(self.exceptionStart)
                pprint.pprint(str(e))
                self.fileWRService.flagOutPut('1', self.filePath.getFlagFilePath())
                return

        self.fileWRService.flagOutPut('2', self.filePath.getFlagFilePath())
        self.fileWRService.logOutPut(self.end, self.filePath.getLogFilePath())
        pprint.pprint(self.end)