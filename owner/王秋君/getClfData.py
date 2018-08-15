# <codecell>

import numpy as np
import pandas as pd
from sklearn import linear_model
from lib.gftTools import gftIO
from functools import reduce     
from datetime import datetime           

from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

from lib.gftTools import gsUtils
from datetime import timedelta


def getClfData(context,x,cutoff):
    dict_x=x[0]
    dict_y=x[1]
    ls_x_dates = list(dict_x.keys())
    ls_y_dates=list(dict_y.keys())
    ls_xy_dates =sorted(list(set(ls_x_dates).intersection(set(ls_y_dates))))
    ##each month end,choose +/- 30% stocks
    dict_xy_merge = {i:Clfcut(dict_x[i],dict_y[i],i,cutoff) for i in ls_xy_dates}
    return dict_xy_merge

def Clfcut(df_x_daily,df_y_daily,i,cutoff):
    df_xy_daily = df_x_daily.merge(df_y_daily,left_index=True,right_index=True,how='inner')
    df_xy_daily=df_xy_daily.rename(columns={i:'y'})
    df_xy_daily_sort = df_xy_daily.sort_values('y').reset_index() 
    cutoff_point = int(df_xy_daily_sort.shape[0]*cutoff)
    
    low_cutoff = df_xy_daily_sort.iloc[cutoff_point,-1]
    high_cutoff = df_xy_daily_sort.iloc[df_xy_daily_sort.shape[0]-cutoff_point,-1]
    
    df_xy_daily_filter=df_xy_daily_sort[(df_xy_daily_sort.y >= high_cutoff) | (df_xy_daily_sort.y <= low_cutoff)]    
    df_xy_daily_filter['newy']=np.where(df_xy_daily_filter['y']>=high_cutoff,1,-1)
    return df_xy_daily_filter

# <codecell>



# <codecell>


