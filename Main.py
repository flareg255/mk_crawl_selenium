from crawlers.FirstCrawler import FirstCrawler
from crawlers.SecondCrawler import SecondCrawler
from crawlers.ThirdCrawler import ThirdCrawler
from crawlers.FourthCrawler import FourthCrawler
from crawlers.FifhCrawler import FifthCrawler

class Main:
    firstCrawler = None
    secondCrawler = None
    thirdCrawler = None
    fourthCrawler = None
    fifthCrawler = None

    def __init__(self):
        # self.firstCrawler = FirstCrawler()
        # self.secondCrawler = SecondCrawler()
        # self.thirdCrawler = ThirdCrawler()
        # self.fourthCrawler = FourthCrawler()
        self.fifthCrawler = FifthCrawler()

    def dataGet(self):
        # self.firstCrawler.firstCatGet()
        # self.secondCrawler.secondCatGet()
        # self.thirdCrawler.thirdCatGet()
        # self.fourthCrawler.fourthCatGet()
        self.fifthCrawler.fifthCatGet()
        # self.secondCrawler.itemsGet()

def main():
    main = Main()
    main.dataGet()

if __name__ == "__main__":
    main()