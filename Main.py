from settings.SetDriver import SetDriver
from crawlers.FirstCrawler import FirstCrawler
from crawlers.SecondCrawler import SecondCrawler
from crawlers.ThirdCrawler import ThirdCrawler
from crawlers.FourthCrawler import FourthCrawler
from crawlers.FifhCrawler import FifthCrawler

from crawlers.ItemsCrawler import ItemsCrawler

class Main:
    setDriver = None
    driver = None

    firstCrawler = None
    secondCrawler = None
    thirdCrawler = None
    fourthCrawler = None
    fifthCrawler = None

    itemsCrawler = None

    def __init__(self):
        self.setDriver = SetDriver()
        self.driver = self.setDriver.getDriver()

        # self.firstCrawler = FirstCrawler(driver=self.driver)
        # self.secondCrawler = SecondCrawler(driver=self.driver)
        # self.thirdCrawler = ThirdCrawler(driver=self.driver)
        # self.fourthCrawler = FourthCrawler(driver=self.driver)
        # self.fifthCrawler = FifthCrawler()

        self.itemsCrawler = ItemsCrawler(driver=self.driver)


    def dataGet(self):
        # self.firstCrawler.firstCatGet()
        # self.secondCrawler.secondCatGet()
        # self.thirdCrawler.thirdCatGet()
        # self.fourthCrawler.fourthCatGet()
        # self.fifthCrawler.fifthCatGet()

        self.itemsCrawler.itemsGet()

        self.driver.quit()

def main():
    main = Main()
    main.dataGet()

if __name__ == "__main__":
    main()