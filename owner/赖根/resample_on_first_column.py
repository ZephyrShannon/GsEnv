# <codecell>

# Your code goes here.
import itertools
import pandas as pd
from datetime import datetime
import numpy as np


def OOTVResample(x):
    df_data=x.asColumnTab()
    #startdate=pd.to_datetime(['1970-01-01'])[0]
    #df_data=df_data[(df_data['T0'] >= startdate)]
    
    ##create a complete date and symbol dataset
    ls_colnames = x.columnOrders
    
    alldates=pd.date_range(start=df_data[ls_colnames[2]].min(),end=datetime.now())
    allsyms=np.unique(df_data[ls_colnames[0]])
    df_alldata=expand_grid({ls_colnames[2]:alldates,ls_colnames[0]:allsyms})
    
    ##merge original dataset:O0 must be the same,T0 is the last key
        
    df_alldata.sort_values(ls_colnames[2],ascending=True,inplace=True)
    df_data.sort_values(ls_colnames[2],ascending=True,inplace=True)
    
    result = pd.merge_asof(df_alldata,
                              df_data, on=ls_colnames[2], by=ls_colnames[0])
    
    result.dropna(subset=[ls_colnames[1]], how='any',inplace=True)
    
    return result

def expand_grid(data_dict):
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())



