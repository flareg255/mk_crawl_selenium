import os
import pandas as pd
import pprint
import datetime

class FileWRService:
    def csvToDataframe(self, filePath):
        df = pd.read_csv(filePath, index_col=0, encoding='cp932', dtype=str)
        return df

    def toCsv(self, datas, fileName):
        df=pd.DataFrame(datas)
        df.to_csv(fileName, encoding='cp932', index=False)

    def catToCsv(self, datas, fileName):
        df=pd.DataFrame(data=datas, columns=['category_name', 'full_category_id', 'first_category_id', 'second_category_id', 'third_category_id', 'fourth_category_id', 'category_depth'])
        df.to_csv(fileName, encoding='cp932')

    def flagOutPut(self, flagStr, filePath):
        fileWriteMode = 'w'
        with open(filePath, fileWriteMode, encoding='UTF-8') as f:
            f.write(flagStr)

    def flagInPut(self, filePath):
        with open(filePath, encoding='UTF-8') as f:
            return f.read()

    def logOutPut(self, logStr, filePath):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)

        fileWriteMode = 'x'
        if os.path.isfile(filePath):
            fileWriteMode = 'a'

        with open(filePath, fileWriteMode, encoding='UTF-8') as f:
            f.write(now.strftime('%Y%m%d%H%M%S') + ' ' + logStr + '\n')
