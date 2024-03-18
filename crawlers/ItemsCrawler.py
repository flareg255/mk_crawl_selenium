from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import re
import time
import pprint

from crawlers.BaseCrawler import BaseCrawler

class ItemsCrawler(BaseCrawler):
    pageCnt = 1
    keys = []
    values = []
    categoryUrl = ''

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.pageCnt = 1
        self.keys = []
        self.values = []
        self.categoryUrl = ''

    def itemsGet(self):
        pprint.pprint('itemsGet start')
        firstCat = self.catergories.getFirstCat(filePath=self.filePath.getCatFilePath(catName='first_cat', layerList=['first_cat']))

        # self.urls.getPageUrl(topCat=catNo,underlayerCat=secondCat[catKey2])
        # for catKey1 in firstCat.keys():
        #     self.dataInit()

        #     catNo = self.getCatNo(firstCat[catKey1])
        #     categoryFullNo = catNo + '00000000000000'

        #     self.categoryUrl = self.urls.getPageUrl(topCat=catNo, underlayerCat=categoryFullNo)
        #     self.recursivePageItemget(url=self.categoryUrl, catKey=catKey1)

        # for catKey1 in firstCat.keys():
        #     secondCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='second_cat_', layerList=[catKey1]))
        #     catNo = self.getCatNo(firstCat[catKey1])

        #     for catKey2 in secondCat.keys():
        #         self.dataInit()

        #         pprint.pprint(self.urls.getPageUrl(topCat=catNo, underlayerCat=secondCat[catKey2]))
        #         catKey = '_'.join([catKey1, catKey2])
        #         self.categoryUrl = self.urls.getPageUrl(topCat=catNo, underlayerCat=secondCat[catKey2])
        #         self.recursivePageItemget(url=self.categoryUrl, catKey=catKey)

        # for catKey1 in firstCat.keys():
        #     secondCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='second_cat', layerList=[catKey1]))
        #     catNo = self.getCatNo(firstCat[catKey1])

        #     for catKey2 in secondCat.keys():
        #         thirdCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='third_cat', layerList=[catKey1, catKey2]))
        #         for catKey3 in thirdCat.keys():
        #             self.dataInit()

        #             pprint.pprint(self.urls.getPageUrl(topCat=catNo, underlayerCat=thirdCat[catKey3]))
        #             catKey = '_'.join([catKey1, catKey2, catKey3])
        #             self.categoryUrl = self.urls.getPageUrl(topCat=catNo, underlayerCat=thirdCat[catKey3])
        #             self.recursivePageItemget(url=self.categoryUrl, catKey=catKey)

        for catKey1 in firstCat.keys():
            secondCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='second_cat', layerList=[catKey1]))
            catNo = self.getCatNo(firstCat[catKey1])

            for catKey2 in secondCat.keys():
                thirdCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='third_cat', layerList=[catKey1, catKey2]))
                for catKey3 in thirdCat.keys():
                    fourthCat = self.catergories.getUnderCat(filePath=self.filePath.getCatFilePath(catName='fourth_cat', layerList=[catKey1, catKey2, catKey3]))
                    for catKey4 in fourthCat.keys():
                        self.dataInit()
                        pprint.pprint(self.urls.getPageUrl(topCat=catNo, underlayerCat=fourthCat[catKey4]))
                        catKey = '_'.join([catKey1, catKey2, catKey3, catKey4])
                        self.categoryUrl = self.urls.getPageUrl(topCat=catNo, underlayerCat=fourthCat[catKey4])
                        self.recursivePageItemget(url=self.categoryUrl, catKey=catKey)

    def recursivePageItemget(self, url, catKey):
        pprint.pprint('recursivePageItemget start')

        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)

        try:
            wait.until(EC.presence_of_all_elements_located)
        except TimeoutException as te:
            pprint.pprint(te)
            try:
                wait.until(EC.presence_of_all_elements_located)
            except TimeoutException as te2:
                pprint.pprint(te2)
                pprint.pprint('再帰的にアイテム取得失敗')
                dictionary = dict(key=self.keys,value=self.values)
                self.fileWRService.toCsv(datas=dictionary, fileName=self.filePath.getItemFilePath(itemName=catKey))
                self.fileWRService.flagOutPut('4', self.filePath.getFlagFilePath())
                return

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
            self.fileWRService.flagOutPut('5', self.filePath.getFlagFilePath())
            return
        else:
            self.itemHtmlToList(elements=self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector()))
            # for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getItemsWrapSelector()):
            #     self.keys.append(re.sub(rtSidRe, '',elem.get_attribute('href').replace(httpUrl, '')))
            #     self.values.append(elem.get_attribute('title'))

            self.pageCnt += 1
            itemNumber = 60 * self.pageCnt

            pprint.pprint(self.urls.getRecursivePageUrl(url=self.categoryUrl, param1=self.pageCnt, param2=itemNumber))
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
