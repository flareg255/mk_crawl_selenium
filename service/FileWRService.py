import pandas as pd
import pprint

class FileWRService:
    def csvToDataframe(self, filePath):
        df = pd.read_csv(filePath, index_col=0, encoding='cp932')
        return df

    def toCsv(self, datas, fileName):
        df=pd.DataFrame(datas)
        df.to_csv(fileName, encoding='cp932')