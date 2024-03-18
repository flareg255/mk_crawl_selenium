from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from service.FileWRService import FileWRService

from settings.SetDriver import SetDriver
from crawlers.FirstCrawler import FirstCrawler
from crawlers.SecondCrawler import SecondCrawler
from crawlers.ThirdCrawler import ThirdCrawler
from crawlers.FourthCrawler import FourthCrawler
from crawlers.FifhCrawler import FifthCrawler

from crawlers.ItemsCrawler import ItemsCrawler
from model.FilePath import FilePath

from items_get.spiders.items_get import ItemsGetSpider

import pprint
from timeout_decorator import TimeoutError

class Main:
    fileWRService = None
    filePath = None
    setDriver = None
    driver = None

    firstCrawler = None
    secondCrawler = None
    thirdCrawler = None
    fourthCrawler = None
    fifthCrawler = None

    itemsCrawler = None

    settings = None
    runner = None
    itemsGetSpider = None

    processFlag = None

    def __init__(self):
        self.fileWRService = FileWRService()
        self.processFlag = 0
        self.filePath = FilePath()

        self.setDriver = SetDriver()
        self.driver = self.setDriver.getDriver()

        self.firstCrawler = FirstCrawler(driver=self.driver)
        self.secondCrawler = SecondCrawler(driver=self.driver)
        self.thirdCrawler = ThirdCrawler(driver=self.driver)
        self.fourthCrawler = FourthCrawler(driver=self.driver)
        # self.fifthCrawler = FifthCrawler()

        self.itemsCrawler = ItemsCrawler(driver=self.driver)

    def dataGet(self):
        self.processFlag = int(self.fileWRService.flagInPut(filePath=self.filePath.getFlagFilePath()))
        pprint.pprint(self.processFlag)
        if self.processFlag == 0:
            try:
                self.firstCrawler.firstCatGet()
            except TimeoutError:
                try:
                    self.firstCrawler.firstCatGet()
                except TimeoutError:
                    pprint.pprint('first time out')
        elif self.processFlag == 1:
            try:
                self.secondCrawler.secondCatGet()
            except TimeoutError:
                try:
                    self.secondCrawler.secondCatGet()
                except TimeoutError:
                    pprint.pprint('second time out')
        elif self.processFlag == 2:
            try:
                self.thirdCrawler.thirdCatGet()
            except TimeoutError:
                try:
                    self.thirdCrawler.thirdCatGet()
                except TimeoutError:
                    pprint.pprint('third time out')
        elif self.processFlag == 3:
            try:
                self.fourthCrawler.fourthCatGet()
            except TimeoutError:
                try:
                    self.fourthCrawler.fourthCatGet()
                except TimeoutError:
                    pprint.pprint('fourth time out')
            # self.fifthCrawler.fifthCatGet()
        elif self.processFlag == 4:
            try:
                self.itemsCrawler.itemsGet()
            except TimeoutError:
                try:
                    self.itemsCrawler.itemsGet()
                except TimeoutError:
                    pprint.pprint('itemsGet time out')

        self.driver.quit()



def main():
    main = Main()
    main.dataGet()

if __name__ == "__main__":
    main()

    fileWRService = FileWRService()
    filePath = FilePath()
    processFlag = fileWRService.flagInPut(filePath=filePath.getFlagFilePath())
    if processFlag == 5:
        settings = get_project_settings()
        configure_logging(settings)
        runner = CrawlerRunner(settings)

        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl()
            reactor.stop()
