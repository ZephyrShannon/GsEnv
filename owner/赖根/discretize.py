# <codecell>

# Your code goes here.
import numpy as np
import pandas as pd

def discretize(df, n=10):
    n = int(n)
    if isinstance(df,gftIO.GftTable):
        df = df.asColumnTab()
    value_column = _findValueColumn(df.columns)
    n_values = df[value_column].values
    out,bins = pd.cut(n_values,n,retbins=True,precision=6)
    # return right side index(not included)
    ls_idx = np.digitize(n_values,bins) 
    ls_dy = []
    for i in range(len(ls_idx)):
        idx = ls_idx[i]-1
        value = None
        if idx >= (len(bins)-1):
            value = bins[idx]
        else:
            value = (bins[idx] + bins[idx+1])/2.0
        ls_dy += [value]
    df[value_column] = ls_dy
    return df
    
def _findValueColumn(ls_columns):
    for acolumn in ls_columns:
        if acolumn.upper() in ["VALUE","VAL","V","Y"]:
            return acolumn
    raise ValueError("Value Column isnot found in {}!".format(ls_columns))


