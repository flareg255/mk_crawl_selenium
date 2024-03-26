from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from model.Urls import Urls
from model.CssSelectors import CssSelectors
from model.Categories import Categories
from model.FilePath import FilePath
from service.FileWRService import FileWRService
from settings.SetDriver import SetDriver

import time
import copy
import pprint
import sys

class BaseCrawler:
    driver = None
    wait = None
    urlGet = None
    baseUrl = ''
    firstUrl = ''
    cssSelectorGet = None
    catergories = None
    filePath = None
    fileWRService = None

    def __init__(self):
        self.setDriver = SetDriver()
        self.driver = self.setDriver.getDriver()

        self.urls = Urls()
        self.baseUrl = self.urls.getBaseUrl()
        self.firstUrl = self.urls.getFirstUrl()

        self.cssSelectors = CssSelectors()

        self.catergories = Categories()

        self.filePath = FilePath()

        self.fileWRService = FileWRService()

    def catDataToCsv(self, url, catKey, execFunction, layers, underLinkSelector):
        pprint.pprint('catDataToCsv')
        self.setDriver = SetDriver()
        self.driver = self.setDriver.getDriver()
        layerList = copy.copy(layers)
        layerList.append(catKey)

        try:
            pprint.pprint(url)
            self.driver.get(url)
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.cssSelectors.getUnderLinkSelector(underLinkSelector))))
        except TimeoutException as te:
            self.fileWRService.logOutPut(execFunction +' TimeoutException1 ' + catKey, self.filePath.getLogFilePath())
            pprint.pprint(execFunction +' TimeoutException1 ' + catKey)
            pprint.pprint(str(te))
            try:
                self.driver.quit()
                self.setDriver = SetDriver()
                self.driver = self.setDriver.getDriver()
                self.driver.get(url)
                wait = WebDriverWait(self.driver, 20)
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.cssSelectors.getUnderLinkSelector(underLinkSelector))))
            except TimeoutException as te2:
                self.driver.quit()
                self.fileWRService.logOutPut(execFunction +' TimeoutException2 ' + catKey, self.filePath.getLogFilePath())
                pprint.pprint(execFunction +' TimeoutException2 ' + catKey)
                pprint.pprint(str(te2))
                # sys.exit()
                return {}

        self.fileWRService.logOutPut(execFunction + ' rendering ' + catKey, self.filePath.getLogFilePath())
        pprint.pprint(execFunction + ' rendering ' + catKey)

        time.sleep(2)

        pprint.pprint('h1 text')
        for elem in self.driver.find_elements(By.CSS_SELECTOR, 'h1'):
            pprint.pprint(elem.text)

        keys = []
        # values = []
        fullCategoryId = []
        firstCategoryId = []
        secondCategoryId = []
        thirdCategoryId = []
        fourthCategoryId = []
        categoryDepth = []
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getUnderLinkSelector(underLinkSelector)):
            if not len(elem.text) == 0 and not elem.text == 'すべて':
                keys.append(elem.text.strip().replace('\u3000', ' '))
                # values.append(elem.get_attribute('value'))

                catNoList = elem.get_attribute('value').split(':')
                fullCategoryId.append(elem.get_attribute('value'))
                if len(catNoList) == 1:
                    firstCategoryId.append(catNoList[0])
                    secondCategoryId.append('')
                    thirdCategoryId.append('')
                    fourthCategoryId.append('')
                elif len(catNoList) == 2:
                    firstCategoryId.append(catNoList[0])
                    secondCategoryId.append(catNoList[1])
                    thirdCategoryId.append('')
                    fourthCategoryId.append('')
                elif len(catNoList) == 3:
                    firstCategoryId.append(catNoList[0])
                    secondCategoryId.append(catNoList[1])
                    thirdCategoryId.append(catNoList[2])
                    fourthCategoryId.append('')
                elif len(catNoList) == 4:
                    firstCategoryId.append(catNoList[0])
                    secondCategoryId.append(catNoList[1])
                    thirdCategoryId.append(catNoList[2])
                    fourthCategoryId.append(catNoList[4])

                categoryDepth.append(underLinkSelector)

        # dictionary = dict(key=keys,value=values)
        dictionary = dict(category_name=keys, full_category_id=fullCategoryId, first_category_id=firstCategoryId, second_category_id=secondCategoryId, third_category_id=thirdCategoryId, fourth_category_id=fourthCategoryId, category_depth=categoryDepth)
        self.fileWRService.toCsv(datas=dictionary, fileName=self.filePath.getCatFilePath(catName=execFunction, layerList=layerList))

        self.driver.quit()
        pprint.pprint('catDataToCsv quit')
        return dictionary

    def getCatNo(self, url):
        httpUrl = self.urls.getBaseUrl()
        catNo = url.replace(httpUrl, '').replace('/', '')

        return catNo
