import os
import pprint
import sys
import shutil
import pandas as pd

from crawlers.BaseCrawler import BaseCrawler

class SecondCrawler(BaseCrawler):
    start = 'secondCatGet start'
    rendering = 'secondCatGet rendering'
    exceptionStart = 'secondCatGet exception----------------------------------------'
    FileNone = 'firstFileNone'
    end = 'secondCatGet end'

    def __init__(self):
        super().__init__()

    def secondCatGet(self):

        prevCat = 'first'
        baseDir = self.filePath.getBaseDirFilePath()
        dataDir = baseDir + prevCat + '_cat/'
        archiveDir = self.filePath.getProcessDirFilePath(cat=prevCat)
        if not len(self.filePath.getDirFilePath(prevCat)) == 0:
            for fileName in self.filePath.getDirFilePath(prevCat):
                firstCat = self.catergories.getUnderCat2(filePath=dataDir + fileName)
                for index, row in firstCat.iterrows():
                    self.catDataToCsv(url=self.urls.getPageUrl(topCat=row['first_category_id'],underlayerCat=''), catKey=index, execFunction='second_cat', layers=[], underLinkSelector='2')

                self.fileWRService.flagOutPut('2', self.filePath.getFlagFilePath())
                self.fileWRService.logOutPut(self.end, self.filePath.getLogFilePath())
                shutil.move(dataDir + fileName, archiveDir + fileName)

                pprint.pprint(self.end)

            return
        else:
            self.fileWRService.flagOutPut('0', self.filePath.getFlagFilePath())
            pprint.pprint(self.FileNone)

            return

