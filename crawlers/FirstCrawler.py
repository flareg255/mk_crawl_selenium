from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import re
import time
import pprint

from crawlers.BaseCrawler import BaseCrawler

class FirstCrawler(BaseCrawler):
    start = 'firstCatGet start'
    rendering = 'firstCatGet rendering'
    exceptionStart = 'firstCatGet exception----------------------------------------'
    end = 'firstCatGet end'

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def firstCatGet(self):
        self.fileWRService.logOutPut(self.start, self.filePath.getLogFilePath())
        pprint.pprint(self.start)
        

        try:
            self.driver.get(self.firstUrl)
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_all_elements_located)
        except TimeoutException as te:
            pprint.pprint(te)
            try:
                self.driver.quit()
                self.driver.get(self.firstUrl)
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_all_elements_located)
            except TimeoutException as te2:
                self.driver.quit()
                self.fileWRService.flagOutPut('0', self.filePath.getFlagFilePath())
                pprint.pprint(te2)
                return

        self.fileWRService.logOutPut(self.rendering, self.filePath.getLogFilePath())
        pprint.pprint(self.rendering)

        time.sleep(2)

        linkText = []
        linkHref = []
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getFirstLinkTextSelector()):
            linkText.append(re.sub(re.compile('<.*?>'), '', elem.get_attribute('innerHTML')))
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getFirstLinkHrefSelector()):
            linkHref.append(re.sub(re.compile('<.*?>'), '', elem.get_attribute('href')))

        dictionary = dict(key=linkText,value=linkHref)

        try:
            self.fileWRService.toCsv(datas=dictionary, fileName=self.filePath.getCatFilePath(catName='first_cat', layerList=['first_cat']))
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