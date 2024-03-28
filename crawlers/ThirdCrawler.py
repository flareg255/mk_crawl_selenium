from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import pprint
import sys
import shutil
import pandas as pd

from crawlers.BaseCrawler import BaseCrawler

class ThirdCrawler(BaseCrawler):
    start = 'thirdCatGet start'
    rendering = 'thirdCatGet rendering'
    FileNone = 'secondFileNone'
    exceptionStart = 'thirdCatGet exception----------------------------------------'
    end = 'thirdCatGet end'

    def __init__(self):
        super().__init__()

    def thirdCatGet(self):
        self.fileWRService.logOutPut(self.start, self.filePath.getLogFilePath())
        pprint.pprint(self.start)

        prevCat = 'second'
        baseDir = self.filePath.getBaseDirFilePath()
        dataDir = baseDir + prevCat + '_cat/'
        archiveDir = self.filePath.getProcessDirFilePath(cat=prevCat)
        if not len(self.filePath.getDirFilePath(prevCat)) == 0:
            for fileName in self.filePath.getDirFilePath(prevCat):
                secondCat = self.catergories.getUnderCat2(filePath=dataDir + fileName)

                fileNameExplode = fileName.split('_')
                catKey1 = fileNameExplode[0].replace('.csv', '')

                for index, row in secondCat.iterrows():
                    catNo = row['first_category_id'][0:3]
                    self.catDataToCsv(url=self.urls.getPageUrl(topCat=catNo, underlayerCat=row['full_category_id']), catKey=index, execFunction='third_cat', layers=[catKey1], underLinkSelector='3')
                shutil.move(dataDir + fileName, archiveDir + fileName)

            self.fileWRService.flagOutPut('3', self.filePath.getFlagFilePath())
            self.fileWRService.logOutPut(self.end, self.filePath.getLogFilePath())
            pprint.pprint(self.end)

            return
        else:
            self.fileWRService.flagOutPut('1', self.filePath.getFlagFilePath())
            pprint.pprint(self.FileNone)

            return