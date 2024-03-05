
from  crawlers.FirstCrawler import FirstCrawler

class Main:
    firstCrawler = None

    def __init__(self):
        self.firstCrawler = FirstCrawler()

    def dataGet(self):
        self.firstCrawler.dataGet()

def main():
    main = Main()
    main.dataGet()

if __name__ == "__main__":
    main()