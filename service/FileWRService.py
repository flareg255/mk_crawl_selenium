import os
import pandas as pd
import pprint
import datetime

class FileWRService:
    def csvToDataframe(self, filePath):
        df = pd.read_csv(filePath, index_col=0, encoding='cp932')
        return df

    def toCsv(self, datas, fileName):
        df=pd.DataFrame(datas)
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
