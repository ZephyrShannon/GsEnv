# <codecell>

import numpy as np
import pandas as pd

def CalCov(context,x,rolling_window):
    df_x=x.asMatrix().iloc[-100:, :5]
    df_x.sort_index(inplace=True)
    #df_x=df_x.ix[1:10,1:5]
    df_cov=pd.rolling_cov(df_x,window=rolling_window)
    ls_factorretcov=list(calcfactorRetCov(df_cov,date) for date in list(df_x.index))
    df_l_factorretcov=pd.concat(ls_factorretcov,axis=0).rename(columns={'variable':'o2'}).reset_index()
    df_l_factorretcov.drop('index',axis=1,inplace=True)
    return df_l_factorretcov

def calcfactorRetCov(df_cov,date):   
    df_onedate=df_cov.T[date]
    df_onedate.columns.name = None
    df_onedate['o1']=df_onedate.index
    df_l_factorretcov = pd.melt(df_onedate,id_vars=['o1'])
    df_l_factorretcov['date']=date
    return df_l_factorretcov
