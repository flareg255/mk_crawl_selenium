from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from model.Urls import Urls
from model.CssSelectors import CssSelectors
from model.Categoris import Categories
from model.FilePath import FilePath

import time
import copy
import pprint


class BaseCrawler:
    driver = None
    wait = None
    urlGet = None
    baseUrl = ''
    firstUrl = ''
    cssSelectorGet = None
    cateries = None
    filePath = None

    def __init__(self):
        self.urls = Urls()
        self.baseUrl = self.urls.getBaseUrl()
        self.firstUrl = self.urls.getFirstUrl()

        self.cssSelectors = CssSelectors()

        self.cateries = Categories()

        self.filePath = FilePath()

    def catDataToCsv(self, url, catKey, execFunction, layers, underLinkSelector):
        layerList = copy.copy(layers)
        layerList.append(catKey)

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

        pprint.pprint(execFunction +' rendering ' + catKey)

        time.sleep(2)

        keys = []
        values = []
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getUnderLinkSelector(underLinkSelector)):
            if not len(elem.text) == 0 and not elem.text == 'すべて':
                keys.append(elem.text.strip().replace('\u3000', ' '))
                values.append(elem.get_attribute('value'))

        dictionary = dict(key=keys,value=values)
        self.cateries.dictToCsv(dataDict=dictionary, fileName=self.filePath.getCatFilePath(catName=execFunction, layerList=layerList))

        return dictionary
