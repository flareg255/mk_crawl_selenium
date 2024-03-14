import sys
sys.path.append('../')

from model.FilePath import FilePath
from model.ItemsData import ItemsData
from model.CssSelectors import CssSelectors
from model.Urls import Urls
from service.FileWRService import FileWRService
from service.StringService import StringService


import scrapy
import os
import pprint
import pandas as pd

class ItemsGetSpider(scrapy.Spider):
    name = "items_get"

    filePath = FilePath()
    itemsData = ItemsData()
    cssSelectors = CssSelectors()
    urls = Urls()
    fileWRService = FileWRService()
    stringService = StringService()
    urlsCategories = []
    resultList = []
    cnt = 0

    def __init__(self):
        itemsList = self.itemsData.itemsGet()
        for items in itemsList:
            path = items.pop(0)
            df = self.fileWRService.csvToDataframe(path)
            for index, row in df.iterrows():
                self.urlsCategories.append([self.urls.getItemsBaseUrl() + str(row['key']), items])

    def start_requests(self):
        urlsCategories = self.urlsCategories.pop(0)
        yield scrapy.Request(urlsCategories[0], callback=self.parse, meta={'category': urlsCategories[1]})

    def parse(self, response):
        urlsCategories = self.urlsCategories.pop(0)
        name = response.css(self.cssSelectors.getProductNameSelector()).get()
        name = self.stringService.spaceReplace(string=name)
        price = response.css(self.cssSelectors.getProductPriceSelector()).get()
        price = self.stringService.priceStringToNumber(price=price)
        detailHtml = self.stringService.spaceAndReturnReplace(response.css(self.cssSelectors.getProductDetailSelector()).get())
        pprint.pprint('============================================')
        pprint.pprint(self.cnt)
        self.resultList.append([name, price, detailHtml] + response.meta['category'])

        # if self.cnt == 200:
        if len(self.urlsCategories) == 0:
            self.fileWRService.toCsv(datas=self.resultList, fileName=self.filePath.getItemFilePath())
            return

        self.cnt += 1
        yield scrapy.Request(urlsCategories[0], callback=self.parse, meta={'category': urlsCategories[1]})
