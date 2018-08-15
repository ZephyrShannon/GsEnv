# <codecell>

from lib.gftTools import gftIO
import pandas as pd
import numpy as np
def GetMaxMinT(A):
    tName = None
    vName = None
    A=A.asColumnTab()
    for colName in list(A.columns):
        if isinstance(A[colName][0], pd.tslib.Timestamp):
            if tName is None:
                tName = colName
        if isinstance(A[colName][0], float):
            if vName is None:
                vName = colName
    A.dropna(axis=0,how='any',subset=[vName], inplace=True)
    if A.shape[0] == 0:
        return pd.DataFrame(data=[[np.nan,np.nan]],columns=['MaxT','MinT'])
    else:
        return pd.DataFrame([[max(A[tName]),min(A[tName])]],columns=['MaxT','MinT'])

# <codecell>



# <codecell>


