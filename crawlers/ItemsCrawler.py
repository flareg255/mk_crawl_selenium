from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import re
import time
import pprint
import shutil
import sys


from crawlers.BaseCrawler import BaseCrawler
from settings.SetDriver import SetDriver

class ItemsCrawler(BaseCrawler):
    pageCnt = 1
    keys = []
    values = []
    categoryUrl = ''
    baseDir = ''
    dataDir = ''
    archiveDir = ''
    fileName = ''
    FileNone = 'fourthFileNone'

    def __init__(self):
        super().__init__()
        self.pageCnt = 1
        self.keys = []
        self.values = []
        self.categoryUrl = ''

    def itemsGet(self):
        pprint.pprint('itemsGet start')
        # firstCat = self.catergories.getFirstCat(filePath=self.filePath.getCatFilePath(catName='first_cat', layerList=['first_cat']))

        prevCat = 'fourth'
        self.baseDir = self.filePath.getBaseDirFilePath()
        self.dataDir = self.baseDir + prevCat + '_cat/'
        self.archiveDir = self.filePath.getArchiveDirFilePath(cat=prevCat)
        categoryDict = self.catergories.getFirstCatString()
        if not len(self.filePath.getDirFilePath(prevCat)) == 0:
            for fileName in self.filePath.getDirFilePath(prevCat):
                self.fileName = fileName
                fileNameExplode = fileName.split('_')

                catNo = categoryDict[fileNameExplode[0]]
                catKey1 = fileNameExplode[0]
                catKey2 = fileNameExplode[1]
                catKey3 = fileNameExplode[2].replace('.csv', '')
                fourthCat = self.catergories.getUnderCat2(filePath=self.dataDir + fileName)
                # for catKey4 in fourthCat.keys():
                for index, row in fourthCat.iterrows():
                    self.dataInit()
                    # pprint.pprint(self.urls.getPageUrl(topCat=catNo, underlayerCat=row['full_category_id']))
                    # catKey = '_'.join([catKey1, catKey2, catKey3, catKey4])
                    self.categoryUrl = self.urls.getPageUrl(topCat=catNo, underlayerCat=row['full_category_id'])
                    self.recursivePageItemget(url=self.categoryUrl, catKey=index)

                shutil.move(self.dataDir + self.fileName, self.archiveDir + self.fileName)

            self.fileWRService.flagOutPut('5', self.filePath.getFlagFilePath())

            self.driver.quit()
            return
        else:
            self.fileWRService.flagOutPut('4', self.filePath.getFlagFilePath())
            pprint.pprint(self.FileNone)

            # self.driver.quit()
            return


        # for catKey1 in firstCat.keys():
        #     secondCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='second_cat', layerList=[catKey1]))
        #     catNo = self.getCatNo(firstCat[catKey1])

        #     for catKey2 in secondCat.keys():
        #         thirdCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='third_cat', layerList=[catKey1, catKey2]))
        #         for catKey3 in thirdCat.keys():
        #             fourthCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='fourth_cat', layerList=[catKey1, catKey2, catKey3]))
                    # for catKey4 in fourthCat.keys():
                    #     self.dataInit()
                    #     pprint.pprint(self.urls.getPageUrl(topCat=catNo, underlayerCat=fourthCat[catKey4]))
                    #     catKey = '_'.join([catKey1, catKey2, catKey3, catKey4])
                    #     self.categoryUrl = self.urls.getPageUrl(topCat=catNo, underlayerCat=fourthCat[catKey4])
                    #     self.recursivePageItemget(url=self.categoryUrl, catKey=catKey)

    def recursivePageItemget(self, url, catKey):
        pprint.pprint('recursivePageItemget start')
        pprint.pprint(url)

        self.setDriver = SetDriver()
        self.driver = self.setDriver.getDriver()
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)

        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector())))
        except TimeoutException as te:
            pprint.pprint(te)
            try:
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector())))
            except TimeoutException as te2:
                pprint.pprint(te2)
                pprint.pprint('再帰的にアイテム取得失敗')
                dictionary = dict(key=self.keys,value=self.values)
                self.fileWRService.toCsv(datas=dictionary, fileName=self.filePath.getItemFilePath(itemName=catKey))
                self.fileWRService.flagOutPut('4', self.filePath.getFlagFilePath())
                sys.exit()
                # return

        pprint.pprint('h1 text')
        for elem in self.driver.find_elements(By.CSS_SELECTOR, 'h1'):
            pprint.pprint(elem.text)

        javascript = 'var cnt = 0;\
        var scrollVal = 0;\
        function scroll() {\
            window.scrollTo(0, document.body.scrollHeight);\
            cnt++;\
            if (cnt == 4) {\
                return;\
            }\
            setTimeout(scroll, 2500);\
        }\
        scroll();'

        self.driver.execute_script(javascript)
        time.sleep(9)

        endFlag = False
        pprint.pprint(len(self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector())))

        if len(self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getBtnNextSelector())) == 0:
            endFlag = True
            self.itemHtmlToList(elements=self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector()))
        elif len(self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector())) == 0:
            endFlag = True
        elif len(self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getNothingDataSelector())) >= 1:
            endFlag = True
        else:
            for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getNextPageBtnSelector()):
                if self.cssSelectors.getBtnDisableSelector() in elem.get_attribute('class'):
                    endFlag = True
                pprint.pprint(elem.get_attribute('class'))

        pprint.pprint('endFlag1')
        pprint.pprint(endFlag)

        if endFlag:
            pprint.pprint('recursivePageItemget end')
            dictionary = dict(key=self.keys,value=self.values)
            self.fileWRService.toCsv(datas=dictionary, fileName=self.filePath.getItemFilePath(itemName=catKey))
            pprint.pprint(self.dataDir + self.fileName)
            pprint.pprint(self.archiveDir + self.fileName)
            self.driver.quit()
            return
        else:
            self.itemHtmlToList(elements=self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector()))
            # for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector()):
            #     self.keys.append(re.sub(rtSidRe, '',elem.get_attribute('href').replace(httpUrl, '')))
            #     self.values.append(elem.get_attribute('title'))

            self.pageCnt += 1
            itemNumber = 60 * self.pageCnt

            pprint.pprint(self.urls.getRecursivePageUrl(url=self.categoryUrl, param1=self.pageCnt, param2=itemNumber))
            self.driver.quit()
            self.recursivePageItemget(url=self.urls.getRecursivePageUrl(url=self.categoryUrl, param1=self.pageCnt, param2=itemNumber), catKey=catKey)

    def dataInit(self):
        self.pageCnt = 1
        self.keys = []
        self.values = []

    def itemHtmlToList(self, elements):
        httpUrl = self.urls.getRemoveUrlString()
        rtSidRe = self.urls.getRemoveQueryRe()

        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector()):
            self.keys.append(re.sub(rtSidRe, '',elem.get_attribute('href').replace(httpUrl, '')))
            self.values.append(elem.get_attribute('title'))
