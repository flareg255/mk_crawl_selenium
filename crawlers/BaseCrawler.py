from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from model.Urls import Urls
from model.CssSelectors import CssSelectors
from model.Categories import Categories
from model.FilePath import FilePath
from service.FileWRService import FileWRService

import time
import timeout_decorator
import copy
import pprint


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
        self.urls = Urls()
        self.baseUrl = self.urls.getBaseUrl()
        self.firstUrl = self.urls.getFirstUrl()

        self.cssSelectors = CssSelectors()

        self.catergories = Categories()

        self.filePath = FilePath()

        self.fileWRService = FileWRService()

    @timeout_decorator.timeout(60)
    def catDataToCsv(self, url, catKey, execFunction, layers, underLinkSelector):
        pprint.pprint('catDataToCsv')
        layerList = copy.copy(layers)
        layerList.append(catKey)

        try:
            self.driver.get(url)
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_all_elements_located)
        except TimeoutException as te:
            self.fileWRService.logOutPut(execFunction +' TimeoutException1 ' + catKey, self.filePath.getLogFilePath())
            pprint.pprint(execFunction +' TimeoutException1 ' + catKey)
            pprint.pprint(str(te))
            try:
                self.driver.quit()
                self.driver.get(url)
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_all_elements_located)
            except TimeoutException as te2:
                self.driver.quit()
                self.fileWRService.logOutPut(execFunction +' TimeoutException2 ' + catKey, self.filePath.getLogFilePath())
                pprint.pprint(execFunction +' TimeoutException2 ' + catKey)
                pprint.pprint(str(te2))
                dictionary = {}
                return dictionary

        self.fileWRService.logOutPut(execFunction +' rendering ' + catKey, self.filePath.getLogFilePath())
        pprint.pprint(execFunction +' rendering ' + catKey)

        time.sleep(2)

        keys = []
        values = []
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getUnderLinkSelector(underLinkSelector)):
            if not len(elem.text) == 0 and not elem.text == 'すべて':
                keys.append(elem.text.strip().replace('\u3000', ' '))
                values.append(elem.get_attribute('value'))

        dictionary = dict(key=keys,value=values)
        self.fileWRService.toCsv(datas=dictionary, fileName=self.filePath.getCatFilePath(catName=execFunction, layerList=layerList))

        return dictionary

    def getCatNo(self, url):
        httpUrl = self.urls.getBaseUrl()
        catNo = url.replace(httpUrl, '').replace('/', '')

        return catNo
