from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import pprint
import sys
import os
import shutil

from crawlers.BaseCrawler import BaseCrawler

class FourthCrawler(BaseCrawler):
    start = 'fourthCatGet start'
    rendering = 'fourthCatGet rendering'
    FileNone = 'thirdFileNone'
    exceptionStart = 'fourthCatGet exception----------------------------------------'
    end = 'fourthCatGet end'

    def __init__(self):
        super().__init__()

    def fourthCatGet(self):
        self.fileWRService.logOutPut(self.start, self.filePath.getLogFilePath())
        pprint.pprint(self.start)

        prevCat = 'third'
        baseDir = self.filePath.getBaseDirFilePath()
        dataDir = baseDir + prevCat + '_cat/'
        archiveDir = self.filePath.getProcessDirFilePath(cat=prevCat)
        categoryDict = self.catergories.getFirstCatString()
        if not len(self.filePath.getDirFilePath(prevCat)) == 0:
            for fileName in self.filePath.getDirFilePath(prevCat):
                fileNameExplode = fileName.split('_')

                catNo = categoryDict[fileNameExplode[0]]
                catKey1 = fileNameExplode[0]
                catKey2 = fileNameExplode[1].replace('.csv', '')
                thirdCat = self.catergories.getUnderCat2(filePath=dataDir + fileName)
                for index, row in thirdCat.iterrows():
                    catNo = row['first_category_id'][0:3]
                    self.catDataToCsv(url=self.urls.getPageUrl(topCat=catNo, underlayerCat=row['full_category_id']), catKey=index, execFunction='fourth_cat', layers=[catKey1,catKey2], underLinkSelector='4')
                shutil.move(dataDir + fileName, archiveDir + fileName)

            self.fileWRService.flagOutPut('4', self.filePath.getFlagFilePath())
            self.fileWRService.logOutPut(self.end, self.filePath.getLogFilePath())
            pprint.pprint(self.end)

            return
        else:
            self.fileWRService.flagOutPut('2', self.filePath.getFlagFilePath())
            pprint.pprint(self.FileNone)

            return