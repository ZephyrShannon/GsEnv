# <codecell>


import numpy as np
import pandas as pd

def FactorreturnToOTV(context,X):
    ls_fexponame=list(map(gftIO.gidInt2Str,list(X['osets'].asColumnTab()['O0'])))
    ind_factor_name=sorted(list(map(gftIO.gidInt2Str,list(X[ls_fexponame[0]].asColumnTab()['O0']))))
    sty_factor_name=sorted(list(map(gftIO.gidInt2Str,list(X[ls_fexponame[1]].asColumnTab()['O0']))))
    dict_factor_map={i+'.ret':i for i in sty_factor_name}
    dict_plot={dict_factor_map[k]: v.rename(columns={list(v.columns)[0]:'factorret'}) for k, v in X.items() if k in list(dict_factor_map.keys())}
    ls_plot=[dict_plot[i].assign(factorname=i).reset_index() for i in dict_plot.keys()]
    df_l_factorret=pd.concat(ls_plot,axis=0)
    df_l_factorret=df_l_factorret.rename(columns={'index':'date'})    
    df_l_factorret['factorname']=list(gftIO.strSet2Np(np.array(df_l_factorret['factorname'])))
    return df_l_factorret

# <codecell>


