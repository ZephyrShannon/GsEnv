# <codecell>


import numpy as np
import pandas as pd

from functools import reduce     
from sklearn.decomposition import PCA

def PCAReduction(context,df_expo,n):
    dict_expo={df_expo[i][0]:df_expo[i][1].asMatrix() for i in range(len(df_expo))} 
    allfactorname=list(dict_expo.keys())
    ls_expo_date=[list(i.index) for i in dict_expo.values()]
    ls_alldates_fexpo=reduce(np.intersect1d,ls_expo_date)
    
    ls_expo_symbol=[i.columns for i in dict_expo.values()]
    ls_symbols_fexpo=reduce(np.union1d,ls_expo_symbol)  
    
    ls_ls_expo=[fexpomerge(df_expo,date,allfactorname,ls_symbols_fexpo)  for date in ls_alldates_fexpo]
    df_expo=pd.concat(ls_ls_expo,axis=0)
    df_expo.dropna(how='any',inplace=True,axis=0)
    
    X=np.array(df_expo.drop(['date'],axis=1))
    pca_result=PCA(n_components=n)
    pca_result.fit(X)
    df_pca_raw=pd.DataFrame(data=pca_result.transform(X),index=df_expo.index).reset_index().rename(columns={'index':'symbol'})
    
    df_date=df_expo[['date']].reset_index().rename(columns={'index':'symbol'})
    df_date=df_expo[['date']].reset_index().drop(['index'],axis=1)
    df_pca=df_pca_raw.merge(df_date,left_index=True,right_index=True)
    return df_pca

def fexpomerge(df_expo,date,allfactorname,ls_symbols_fexpo):
    ls_raw_df_fexpo=[df_expo[i][1].asMatrix().reindex(index=[date],columns=ls_symbols_fexpo).rename(index={date:df_expo[i][0]}) for i in range(len(allfactorname))] 
    df_fexpo_onedate=pd.concat(ls_raw_df_fexpo,axis=0).T.assign(date=date)
    return df_fexpo_onedate

# <codecell>



# <codecell>



# <codecell>


