# <codecell>

import pandas as pd



def average(axis, name, dataframe):
    if isinstance(dataframe, gftIO.GftTable):
        if dataframe.matrix is not None:
            dataframe = dataframe.matrix
        else:
            dataframe = dataframe.columnTab
    ret = dataframe.mean(axis=axis, skipna=True)
    if ret.shape[0] == 1:
        return ret.values[0]
    else:
        return pd.DataFrame(data=ret.values, index= ret.index, columns=[name])
    



# <codecell>

