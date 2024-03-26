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
        archiveDir = self.filePath.getArchiveDirFilePath(cat=prevCat)
        # categoryDict = self.catergories.getFirstCatString()
        if not len(self.filePath.getDirFilePath(prevCat)) == 0:
            for fileName in self.filePath.getDirFilePath(prevCat):
                # fileNameExplode = fileName.split('_')

                # catKey1 = fileNameExplode[0].replace('.csv', '')
                # catNo = categoryDict[catKey1]
                # firstCat = self.catergories.getUnderCat2(filePath=dataDir + fileName, cat=prevCat + '_category_id')
                # pprint.pprint(firstCat)
                # for catKey2 in firstCat.keys():
                #     pprint.pprint(firstCat[catKey2])
                #     # try:
                #     self.catDataToCsv(url=self.urls.getPageUrl(topCat=catNo,underlayerCat=secondCat[catKey2]), catKey=catKey2, execFunction='third_cat', layers=[catKey1], underLinkSelector='3')
                #     # except Exception as e:
                #     #     self.driver.quit()
                #     #     self.fileWRService.logOutPut(str(e), self.filePath.getLogFilePath())
                #     #     pprint.pprint(self.exceptionStart)
                #     #     pprint.pprint(str(e))
                #     #     try:
                #     #         self.catDataToCsv(url=self.urls.getPageUrl(topCat=catNo,underlayerCat=secondCat[catKey2]), catKey=catKey2, execFunction='third_cat', layers=[catKey1], underLinkSelector='3')
                #     #     except Exception as e:
                #     #         self.driver.quit()
                #     #         self.fileWRService.logOutPut(str(e), self.filePath.getLogFilePath())
                #     #         pprint.pprint(self.exceptionStart)
                #     #         pprint.pprint(str(e))
                #     #         self.fileWRService.flagOutPut('1', self.filePath.getFlagFilePath())
                #     #         sys.exit()
                # shutil.move(dataDir + fileName, archiveDir + fileName)



        # self.fileWRService.logOutPut(self.start, self.filePath.getLogFilePath())
        # pprint.pprint(self.start)

        # secondFilePath = self.filePath.getCatFilePath(catName='first_cat', layerList=['first_cat'])
        # if os.path.isfile(secondFilePath):
            # firstCat = self.catergories.getFirstCat(filePath=secondFilePath)
                firstCat = self.catergories.getUnderCat2(filePath=dataDir + fileName)
                for index, row in firstCat.iterrows():
                # for catKey in firstCat.keys():
                    # pprint.pprint(firstCat[catKey])
                    # try:
                    self.catDataToCsv(url=self.urls.getPageUrl(topCat=row['first_category_id'],underlayerCat=''), catKey=index, execFunction='second_cat', layers=[], underLinkSelector='2')
                    # except Exception as e:
                    #     self.fileWRService.logOutPut(str(e), self.filePath.getLogFilePath())
                    #     pprint.pprint(self.exceptionStart)
                    #     pprint.pprint(str(e))
                    #     self.fileWRService.flagOutPut('1', self.filePath.getFlagFilePath())
                    #     sys.exit()

                self.fileWRService.flagOutPut('2', self.filePath.getFlagFilePath())
                self.fileWRService.logOutPut(self.end, self.filePath.getLogFilePath())
                shutil.move(dataDir + fileName, archiveDir + fileName)
                # self.driver.quit()
                pprint.pprint(self.end)

            return
        else:
            self.fileWRService.flagOutPut('0', self.filePath.getFlagFilePath())
            pprint.pprint(self.FileNone)

            return

