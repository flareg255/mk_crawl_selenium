
from crawlers.FirstCrawler import FirstCrawler
from crawlers.SecondCrawler import SecondCrawler

class Main:
    firstCrawler = None
    secondCrawler = None

    def __init__(self):
        self.firstCrawler = FirstCrawler()
        self.secondCrawler = SecondCrawler()

    def dataGet(self):
        # self.firstCrawler.hrefGet()
        # self.secondCrawler.secondCatGet()
        self.secondCrawler.itemsGet()

def main():
    main = Main()
    main.dataGet()

if __name__ == "__main__":
    main()