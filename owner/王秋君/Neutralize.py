# <codecell>

import numpy as np
import pandas as pd
from datetime import datetime as dt
from functools import reduce
def Neutralize(context,riskX):
    
    dict_risk_expo=riskX
    ls_fexponame=list(map(gftIO.gidInt2Str,list(dict_risk_expo['osets'].asColumnTab()['O0'])))
    
    ind_factor_name=sorted(list(map(gftIO.gidInt2Str,list(dict_risk_expo[ls_fexponame[0]].asColumnTab()['O0']))))
    sty_factor_name=['B9CCDA635F039E84D489F964DB08BC5C']##规模因子暴露
    allfactor =ind_factor_name +sty_factor_name
    
    dict_risk_expo_new = {factorname: dict_risk_expo[factorname].asMatrix() for factorname in allfactor}
    ##get needed date
    ls_ls_fexpodate=list([dict_risk_expo_new[factorname].index.tolist() for factorname in dict_risk_expo_new.keys()]) 
    ls_alldates_fexpo=reduce(np.intersect1d,ls_ls_fexpodate)
    
    df_alldates = pd.DataFrame(data=ls_alldates_fexpo,columns=['date'])
    df_alldates['year']=df_alldates['date'].dt.year
    df_alldates['month']=df_alldates['date'].dt.month
    ls_final_dates = list(df_alldates.groupby(['year','month'])['date'].max())
    ##get needed symbol
    ls_ls_fexposymbol=list([dict_risk_expo_new[factorname].columns.tolist() for factorname in dict_risk_expo_new.keys()]) 
    ls_allsymbols=reduce(np.intersect1d,ls_ls_fexposymbol)
    
    ##get final industry and size factor
    dict_df_fexpo_raw ={date:fexpomerge(dict_risk_expo_new,date,allfactor,ls_allsymbols) for date in ls_final_dates}  
    return dict_df_fexpo_raw

def fexpomerge(dict_risk_expo_new,date,allfactor,ls_allsymbols):
    ls_raw_df_fexpo=[dict_risk_expo_new[factorname].reindex(index=[date],columns=ls_allsymbols).rename(index={date:factorname}) for factorname in allfactor] 
    df_fexpo_onedate=pd.concat(ls_raw_df_fexpo,axis=0).T
    return df_fexpo_onedate

# <codecell>


