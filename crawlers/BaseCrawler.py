from settings.SetDriver import SetDriver
from model.Urls import Urls
from model.CssSelectors import CssSelectors
from model.Categoris import Categories
from model.FilePath import FilePath

class BaseCrawler:
    setDriver = None
    driver = None
    wait = None
    urlGet = None
    baseUrl = ''
    firstUrl = ''
    cssSelectorGet = None
    cateries = None
    filePath = None

    def __init__(self):
        self.setDriver = SetDriver()
        self.driver = self.setDriver.getDriver()

        self.urls = Urls()
        self.baseUrl = self.urls.getBaseUrl()
        self.firstUrl = self.urls.getFirstUrl()

        self.cssSelectors = CssSelectors()

        self.cateries = Categories()

        self.filePath = FilePath()