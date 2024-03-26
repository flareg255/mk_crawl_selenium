from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import os
import re
import time
import pprint
import sys

from crawlers.BaseCrawler import BaseCrawler
# from settings.SetDriver import SetDriver

class FirstCrawler(BaseCrawler):
    driver = None
    wait = None
    start = 'firstCatGet start'
    rendering = 'firstCatGet rendering'
    exceptionStart = 'firstCatGet exception----------------------------------------'
    end = 'firstCatGet end'

    def __init__(self):
        super().__init__()

    def firstCatGet(self):
        self.fileWRService.logOutPut(self.start, self.filePath.getLogFilePath())
        pprint.pprint(self.start)

        try:
            self.driver.get(self.firstUrl)
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.cssSelectors.getFirstLinkTextSelector())))
        except TimeoutException as te:
            pprint.pprint('TimeoutException')
            pprint.pprint(te)
            try:
                self.driver.quit()
                self.driver.get(self.firstUrl)
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.cssSelectors.getFirstLinkTextSelector())))
            except TimeoutException as te2:
                self.driver.quit()
                self.fileWRService.flagOutPut('0', self.filePath.getFlagFilePath())
                pprint.pprint(te2)
                sys.exit()

        pprint.pprint('h1 text')
        for elem in self.driver.find_elements(By.CSS_SELECTOR, 'h1'):
            pprint.pprint(elem.text)

        self.fileWRService.logOutPut(self.rendering, self.filePath.getLogFilePath())
        pprint.pprint(self.rendering)

        time.sleep(2)

        linkText = []
        linkHref = []
        firstCategoryId = []
        secondCategoryId = []
        thirdCategoryId = []
        fourthCategoryId = []
        categoryDepth = []
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getFirstLinkTextSelector()):
            linkText.append(re.sub(re.compile('<.*?>'), '', elem.get_attribute('innerHTML')))
            categoryDepth.append(1)
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getFirstLinkHrefSelector()):
            catNo = self.urls.getCatgoryNo(elem.get_attribute('href'))
            linkHref.append(catNo)
            firstCategoryId.append(catNo)
            secondCategoryId.append('')
            thirdCategoryId.append('')
            fourthCategoryId.append('')

        # dictionary = dict(key=linkText,value=linkHref)
        dictionary = dict(category_name=linkText, full_category_id=linkHref, first_category_id=firstCategoryId, second_category_id=secondCategoryId, third_category_id=thirdCategoryId, fourth_category_id=fourthCategoryId, category_depth=categoryDepth)

        dictionary = self.catergories.firstCatFilter(dictionary)
        # pprint.pprint(dictionary)

        try:
            firstFilePath = self.filePath.getCatFilePath(catName='first_cat', layerList=['first_cat'])
            self.fileWRService.toCsv(datas=dictionary, fileName=firstFilePath)
        except Exception as e:
            self.fileWRService.logOutPut(self.exceptionStart, self.filePath.getLogFilePath())
            pprint.pprint(self.exceptionStart)
            self.fileWRService.logOutPut(str(e), self.filePath.getLogFilePath())
            pprint.pprint(str(e))
            self.fileWRService.flagOutPut('0', self.filePath.getFlagFilePath())
            return

        self.fileWRService.flagOutPut('1', self.filePath.getFlagFilePath())
        self.fileWRService.logOutPut(self.end, self.filePath.getLogFilePath())
        pprint.pprint(self.end)

        self.driver.quit()

        return