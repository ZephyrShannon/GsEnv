# <codecell>

import itertools
import pandas as pd
from datetime import datetime
import numpy as np

def OOTVResamplewithFreq(context,x,freq):
    df_data=x.asColumnTab()
    ##create a complete date and symbol dataset
    column_type= gftIO.get_columns_type_dict(df_data)
    columns = []
    for key in column_type:
            if column_type[key]==2:
                df_data.rename(columns={key:'date'}, inplace=True)
            elif column_type[key]==23:
                df_data.rename(columns={key:'value'}, inplace=True)
            elif column_type[key]==4: 
                columns.append(key)
    df_data.rename(columns={columns[0]:'symbol'}, inplace=True)
    df_data.rename(columns={columns[1]:'industry'}, inplace=True)
    alldates=freq
    allsyms=np.unique(df_data['symbol'])
    df_alldata=expand_grid({'date':alldates,'symbol':allsyms})
     ##merge original dataset:O0 must be the same,T0 is the last key
    df_alldata.sort_values('date',ascending=True,inplace=True)
    df_data.sort_values('date',ascending=True,inplace=True)
    result = pd.merge_asof(df_alldata,
                                  df_data, on= 'date', by= 'symbol')
    result.dropna(subset=['industry'], how='any',inplace=True)
    return result

def expand_grid(data_dict):
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())
