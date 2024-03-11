import pandas as pd
import pprint

class FileWRService():

    def dictToCsv(self, dataDict, fileName):
        df=pd.DataFrame(dataDict)
        df.to_csv(fileName, encoding='cp932')