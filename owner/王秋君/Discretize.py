# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gftIO
from lib.gftTools import gsUtils
def Discretize(context,data,binnumber,asc):
    df_data=data.asColumnTab()
    ser_missingvalue = pd.isnull(df_data).sum(axis=0)/df_data.shape[0]
    ls_xy_name = ser_missingvalue[ser_missingvalue < 0.3].index.tolist()
    df_data_fnl=df_data.reindex(columns=ls_xy_name)
    
    ls_date =np.unique(list(df_data_fnl.date))
    discretname=[i for i in ls_xy_name if i not in ['symbol','y','date']]
    if asc==1:
        asc=True
    else:
        asc=False        
    for key in ls_date:
        temp=df_data_fnl[df_data_fnl.date == key].copy()
        temp.fillna(temp.mean(),inplace=True)
        temp[discretname]=pd.DataFrame(temp[discretname].apply(lambda x:gsUtils.cut2bin(x,binnumber,ascending=asc)),dtype='float')
        df_data_fnl[df_data_fnl.date == key]=temp 
    return df_data_fnl

# <codecell>


