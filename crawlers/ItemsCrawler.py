from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import re
import time
import pprint
import shutil
import sys
import os


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
    FileNone = ' FileNone'

    def __init__(self):
        super().__init__()
        self.pageCnt = 1
        self.keys = []
        self.values = []
        self.categoryUrl = ''

    def itemsGet(self, layer):
        pprint.pprint('itemsGet start')

        layers = ['first','second','third','fourth']
        baseLayer = 5
        catlayer = layers[layer]
        self.baseDir = self.filePath.getBaseDirFilePath()
        self.dataDir = self.filePath.getProcessDirFilePath(cat=catlayer)
        self.archiveDir = self.filePath.getArchiveDirFilePath(cat=catlayer)
        # categoryDict = self.catergories.getFirstCatString()
        if not len(os.listdir(self.dataDir)) == 0:
            for fileName in os.listdir(self.dataDir):
                # self.fileName = fileName
                # fileNameExplode = fileName.split('_')

                # catNo = categoryDict[fileNameExplode[0]]
                # catDf = self.catergories.getUnderCat2(filePath=self.dataDir + fileName)
                catDf = self.fileWRService.csvToDataframe(self.dataDir + fileName)

                for index, row in catDf.iterrows():
                    catNo = row['first_category_id'][0:3]
                    self.dataInit()

                    if catlayer == 'first':
                        self.categoryUrl = self.urls.getPageUrl(topCat=catNo, underlayerCat=str(catNo) + '00000000000000')
                    else:
                        self.categoryUrl = self.urls.getPageUrl(topCat=catNo, underlayerCat=row['full_category_id'])
                    self.recursivePageItemget(url=self.categoryUrl, catKey=index)

                shutil.move(self.dataDir + self.fileName, self.archiveDir + self.fileName)

                if len(os.listdir(self.dataDir)) == 0:
                    nextLayer = baseLayer + layer
                    self.fileWRService.flagOutPut(nextLayer, self.filePath.getFlagFilePath())

                self.driver.quit()
                return
        else:
            nextLayer = baseLayer + layer - 1
            self.fileWRService.flagOutPut(str(nextLayer), self.filePath.getFlagFilePath())
            pprint.pprint(self.dataDir + self.FileNone)

            return

    def recursivePageItemget(self, url, catKey):
        pprint.pprint('recursivePageItemget start')
        pprint.pprint(url)

        self.setDriver = SetDriver()
        self.driver = self.setDriver.getDriver()
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 30)

        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector())))
        except TimeoutException as te:
            pprint.pprint(te)
            try:
                self.driver.quit()
                self.setDriver = SetDriver()
                self.driver = self.setDriver.getDriver()
                self.driver.get(url)
                wait = WebDriverWait(self.driver, 30)
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector())))
            except TimeoutException as te2:
                pprint.pprint(te2)
                pprint.pprint('再帰的にアイテム取得失敗')
                pprint.pprint(url)
                dictionary = dict(key=self.keys,value=self.values)
                self.fileWRService.toCsv(datas=dictionary, fileName=self.filePath.getItemFilePath(itemName=catKey))
                self.fileWRService.flagOutPut('4', self.filePath.getFlagFilePath())
                self.driver.quit()
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

            self.driver.quit()
            pprint.pprint('self.driver.quit()')
            return
        else:
            self.itemHtmlToList(elements=self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector()))

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
