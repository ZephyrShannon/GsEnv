# <codecell>

import numpy as np
import pandas as pd
from sklearn import linear_model
from lib.gftTools import gftIO
from functools import reduce     
from datetime import datetime           

from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

def GetRetData(context,Y,X):
    ##step1:get stock return date range,stock list
    df_y=Y
    df_x=X
    df_y=df_y.asMatrix()
    ls_y_date_range=list(df_y.index)
    
    ##step2:get factor loading,factorname,date range,stock list
    dict_x={df_x[i][0]:df_x[i][1].asMatrix() for i in range(len(df_x))}   
    dict_datelength={i:len(j.index) for i,j in dict_x.items()}
    float_quantile=np.percentile(a=(list(dict_datelength.values())),q=5)
    dict_x={k: v for k, v in dict_x.items() if len(v.index) >= float_quantile}
    ls_allfactor_name=list(dict_x.keys())
    ls_x_date=[list(i.index) for i in dict_x.values()]
    ls_alldates_x=reduce(np.intersect1d,ls_x_date)  
    
    ##step3:get date mapping for regression
    df_date_mapping=pd.DataFrame(data=ls_y_date_range,columns=['ret_date'])
    df_date_mapping['x_date']=df_date_mapping.shift(1)
    df_date_mapping_fnl = df_date_mapping[df_date_mapping.x_date.isin(list(ls_alldates_x))].copy()
    
    ##step4:get all symbols for regression,prepare all x/y data
    ls_y_dates= list(df_date_mapping_fnl.ret_date)      
    dict_symbol={date: np.unique(df_y[df_y.index == date].T.dropna().index) for date in ls_y_dates}
    
    dict_x={date:x_merge(df_x,date,ls_allfactor_name,dict_symbol,df_date_mapping)  for date in ls_y_dates}
    dict_y={date:df_y[df_y.index == date].T.reindex(index=dict_symbol[date]) for date in ls_y_dates}
    
    dict_expo_filter={k: missingpre(v) for k, v in dict_x.items()}###会导致每天的因子个数不
    dict_expo_std={k: (v -v.mean(axis=0))/v.std(axis=0) for k, v in dict_expo_filter.items()}
    dict_expo_std_new={k: v.apply(lambda x:x-min(x)/(max(x)-min(x))) for k, v in dict_expo_std.items()}
    return (dict_expo_std_new,dict_y)
        
def x_merge(df_x,date,ls_allfactor_name,dict_symbol,df_date_mapping):
    x_date=list(df_date_mapping[df_date_mapping.ret_date == date].x_date)[0]
    ls_raw_df_x=[df_x[i][1].asMatrix().reindex(index=[x_date],columns=dict_symbol[date]).rename(index={x_date:df_x[i][0]}) for i in range(len(ls_allfactor_name))] 
    df_x_onedate=pd.concat(ls_raw_df_x,axis=0).T
    return df_x_onedate
def missingpre(v):
    df_expoonedate=v
    if len(df_expoonedate.columns) != len(np.unique(df_expoonedate.columns)):
        df_expoonedate=df_expoonedate.T.reset_index()
        df_expoonedate=df_expoonedate.drop_duplicates(subset='index').set_index(['index']).T
    dict_missingrate ={i:df_expoonedate[i].count()/df_expoonedate.shape[0] for i in list(df_expoonedate.columns)}
    dict_missingrate_filter={m: n for m,n in dict_missingrate.items() if n >= 0.8}
    ls_leftfactor=list(dict_missingrate_filter.keys())
    
    df_expoonedate_del=df_expoonedate.reindex(columns=ls_leftfactor)
    df_expoonedate_del=df_expoonedate_del.fillna(df_expoonedate_del.mean(axis=0,skipna=True))
    return df_expoonedate_del

# <codecell>



# <codecell>


