from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import re
import time
import pprint

from crawlers.BaseCrawler import BaseCrawler

class FirstCrawler(BaseCrawler):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def firstCatGet(self):
        pprint.pprint('firstCatGet start')
        self.driver.get(self.firstUrl)
        wait = WebDriverWait(self.driver, 10)

        try:
            wait.until(EC.presence_of_all_elements_located)
        except TimeoutException as te:
            pprint.pprint(te)
            try:
                wait.until(EC.presence_of_all_elements_located)
            except TimeoutException as te2:
                pprint.pprint(te2)
        pprint.pprint('firstCatGet rendering')

        time.sleep(2)

        linkText = []
        linkHref = []
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getFirstLinkTextSelector()):
            linkText.append(re.sub(re.compile('<.*?>'), '', elem.get_attribute('innerHTML')))
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectors.getFirstLinkHrefSelector()):
            linkHref.append(re.sub(re.compile('<.*?>'), '', elem.get_attribute('href')))

        dictionary = dict(key=linkText,value=linkHref)

        self.fileWRService.dictToCsv(dataDict=dictionary, fileName=self.filePath.getCatFilePath(catName='first_cat', layerList=['first_cat']))

        pprint.pprint('firstCatGet end')