# <codecell>

import numpy as np
import pandas as pd

def filter_value(context, data, value, how):
    if isinstance(data, gftIO.GftTable):
        if data.columnTab is not None:
            return filter_col_tab(data.columnTab, value, how)
        else:
            return filter_mat(data.matrix, value, how)
    elif isinstance(data, pd.DataFrame):
        if gftIO.ismatrix(data):
            return filter_mat(data, value, how)
        else:
            return filter_col_tab(data, value, how)
        
def filter_mat(data, value, how):
    ret = data.copy()
    ret[ret=value] = np.nan
    return ret

def filter_col_tab(data, value, how):
    ret = data.copy()
    ret[ret['V']== value] = np.nan
    ret.dropna()
    return ret
    
