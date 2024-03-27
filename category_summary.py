import os
import pprint
import copy
import pandas as pd

targetDirPaths = ['first_cat', 'second_cat', 'third_cat', 'fourth_cat', 'items']
pathList = []
pathList.append(os.getcwd())
pathList.append('data')
pathList.append('archive')

cols = ['category_name', 'full_category_id', 'first_category_id', 'second_category_id', 'third_category_id', 'fourth_category_id', 'category_depth']
resultDf = pd.DataFrame(index=[], columns=cols)

for targetDir in targetDirPaths:
    pathList.append(targetDir)
    # pprint.pprint(os.listdir(os.path.join(*pathList)))

    for innerPath in os.listdir(os.path.join(*pathList)):
        innerPathList = copy.deepcopy(pathList)
        innerPathList.append(innerPath)
        filePath = os.path.join(*innerPathList)

        df = pd.read_csv(filePath, encoding='cp932', dtype=str)
        resultDf = pd.concat([resultDf, df], ignore_index=False)

    pathList = pathList[:-1]
pprint.pprint(df)
resultDf.to_csv('./test.csv', encoding='cp932', index=False)

