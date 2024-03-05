from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import pandas as pd

import re
import time
import pprint

from crawlers.BaseCrawler import BaseCrawler

class FirstCrawler(BaseCrawler):
    def firstCatGet(self):
        self.driver.get(self.firstUrl)
        wait = WebDriverWait(self.driver, 10)

        time.sleep(2)

        linkText = []
        linkHref = []
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectorGet.getFirstLinkTextSelector()):
            linkText.append(re.sub(re.compile('<.*?>'), '', elem.get_attribute('innerHTML')))
        for elem in self.driver.find_elements(By.CSS_SELECTOR, self.cssSelectorGet.getFirstLinkHrefSelector()):
            linkHref.append(re.sub(re.compile('<.*?>'), '', elem.get_attribute('href')))

        dictionary = dict(key=linkText,value=linkHref)

        df=pd.DataFrame(dictionary)
        df.to_csv('./data/first_cat.csv', header=False, index=False, encoding='cp932')

        self.driver.quit()