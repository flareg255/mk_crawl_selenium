from settings.SetDriver import SetDriver
from const.UrlGet import UrlGet
from const.CssSelectorGet import CssSelectorGet

class BaseCrawler:
    setDriver = None
    driver = None
    wait = None
    urlGet = None
    firstUrl = ''
    cssSelectorGet = None

    def __init__(self):
        self.setDriver = SetDriver()
        self.driver = self.setDriver.getDriver()

        self.urlGet = UrlGet()
        self.firstUrl = self.urlGet.getFirstUrl()

        self.cssSelectorGet = CssSelectorGet()