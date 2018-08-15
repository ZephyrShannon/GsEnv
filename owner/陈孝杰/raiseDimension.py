# <codecell>

import numpy as np
import pandas as pd

def raiseDimension(tableList,targetGidList):
    result = None
    if targetGidList is None:
        for i in range(len(tableList)):
            gid = tableList[i][0]
            table = tableList[i][1]
            df = table.asColumnTab().copy()
            if table.isNonSymbol():
                if 'variable' in df.columns:
                    del df['variable']
            df['groupID'] = gid
            result = pd.concat([result, df], axis=0)
    else:
        if len(tableList) != len(targetGidList):
            raise Exception("tableList and targetGidList have different length")
        for i in range(len(tableList)):
            gid = targetGidList[i][0]
            table = tableList[i][1]
            df = table.asColumnTab().copy()
            if table.isNonSymbol():
                if 'variable' in df.columns:
                    del df['variable']
            df['groupID'] = gid
            result = pd.concat([result, df], axis=0)
    return result
