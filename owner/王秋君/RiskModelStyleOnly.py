# <codecell>



# <codecell>


import numpy as np
import pandas as pd
from functools import reduce

import statsmodels.api as sm
#import matplotlib.pyplot as plt
#from statsmodels.sandbox.regression.predstd import wls_prediction_std
from lib.gftTools import gftIO
import datetime

##gidnew:CBAD472792D91D18D6138F0F9AAE4C15

def RiskModelStyleOnly(df_ret,dict_risk_expo,period):
    '''
    df_ret=x0
    dict_risk_expo=x1
    period=5
    '''
    period=int(period['CovWindow'])
    
    ls_fexponame=list(map(gftIO.gidInt2Str,list(dict_risk_expo['osets'].asColumnTab()['O0'])))
    allfactor=[]
    for i in ls_fexponame:
        allfactor.extend(list(map(gftIO.gidInt2Str,list(dict_risk_expo[i].asColumnTab()['O0']))))
    
    ##stock return preprocess
    df_w_ret=df_ret.asMatrix().T.dropna(how='all',axis=1)
    
    ##factor exposure preprocess
    dict_risk_expo_new = {factorname: dict_risk_expo[factorname].asMatrix() for factorname in allfactor}
    ls_ls_fexpodate=list([dict_risk_expo_new[factorname].index.tolist() for factorname in dict_risk_expo_new.keys()]) 
    ls_alldates_fexpo=reduce(np.intersect1d,ls_ls_fexpodate)
    
    ls_ls_fexposymbol=list([dict_risk_expo_new[factorname].columns.tolist() for factorname in dict_risk_expo_new.keys()]) 
    ls_allsymbols_fexpo=reduce(np.intersect1d,ls_ls_fexposymbol)
    
    
    
    ##get fexpo date,find the nearest business day
    
    fexpodate=pd.DataFrame(ls_alldates_fexpo,columns=['date_fexpo'])
    retdate=pd.DataFrame(df_w_ret.columns,columns=['date_ret'])
    
    retdate.sort_values("date_ret",ascending=True,inplace=True)
    fexpodate.sort_values("date_fexpo",ascending=True,inplace=True)
    
    df_date_map = pd.merge_asof(retdate,
                              fexpodate, left_on ="date_ret",right_on ="date_fexpo",allow_exact_matches=False)
    
    df_date_map.dropna(how='any',inplace=True)
    df_date_map=df_date_map.drop_duplicates(subset='date_fexpo').reset_index()    
    dict_date_map={df_date_map.date_fexpo[i]:df_date_map.date_ret[i] for i in range(len(df_date_map))}
    
    
    
    ##get the date intersection of stock return and factor exposure
    ls_alldates=set(df_w_ret.columns).intersection(set(dict_date_map.values()))
    ls_alldates_ondaybefore=sorted(list(dict_date_map.keys()))
    ls_allsymbols={date: list(set(df_w_ret[[dict_date_map[date]]].dropna().index).intersection(set(ls_allsymbols_fexpo))) for date in ls_alldates_ondaybefore}
    
    #align the stock return and factor exposure
    dict_df_ret={dict_date_map[date]: df_w_ret[[dict_date_map[date]]].reindex(index=ls_allsymbols[date]) for date in ls_alldates_ondaybefore}
    dict_df_fexpo ={date:fexpomerge(dict_risk_expo_new,date,allfactor,ls_allsymbols) for date in ls_alldates_ondaybefore}  
 

    
    #for i in dict_risk_expo_new.keys():
        #if dict_risk_expo_new[i].index.min() > df_l_ret.index.min() or dict_risk_expo_new[i].index.max() < df_l_ret.index.max():
            #raise Exception
            
    ########################step3:calculate factor return########################
    

    ls_df_fitresult={dict_date_map[date]:Regression(date,dict_df_ret,dict_df_fexpo,dict_date_map) for date in ls_alldates_ondaybefore}
    
    ls_df_facreturn=list(ls_df_fitresult[date]['params'].rename(columns={'params':date}) for date in ls_alldates)
    df_model_params=reduce(lambda df_para1,df_para2:pd.concat([df_para1,df_para2],axis=1),ls_df_facreturn)
    
    ########################step4:calculate factor return covariance########################  
    
    df_allfactorret=df_model_params.T
    df_allfactorret=df_allfactorret.sort_index()
    
    panel_factorretcov=pd.rolling_cov(df_allfactorret,window=period)


    ls_factorretcov=list(calcfactorRetCov(panel_factorretcov,date,allfactor) for date in list(df_allfactorret.index))
    df_l_factorretcov=pd.concat(ls_factorretcov,axis=0).rename(columns={'variable':'factorid2'})
                                  
    ########################step5:calculate the residual(specific) variances of regression########################
    
    ##part1:merge factorreturn,factor exposure and stock return
    ls_specificrisk=list(ls_df_fitresult[date]['resid'].rename(columns={'resid':date}) for date in ls_alldates)
    df_w_specificrisk=pd.concat(ls_specificrisk,axis=1).T
    df_w_specificrisk=df_w_specificrisk.sort_index()
    df_specificrisk_var =pd.rolling_var(df_w_specificrisk,window=period) 
    df_specificrisk_var['idname'] = df_specificrisk_var.index
    df_specificrisk_var=pd.melt(df_specificrisk_var, id_vars=['idname'])
    df_specificrisk_var=df_specificrisk_var.rename(columns={'idname':'date','variable':'symbol','value':'specificrisk'})              

    ########################step6:generate final return value########################
    
    dict_factorret={key+'.ret': df_allfactorret[[key]].rename(columns={key:list(gftIO.strSet2Np(np.array(list(df_allfactorret[[key]].columns))))[0]}) for key in df_allfactorret.columns}

    dictMerged=dict(dict_factorret, **dict_risk_expo, **{'ret_cov':df_l_factorretcov,'specificRisk':df_specificrisk_var})                      
    #gftIO.zdump(dictMerged,'riskmodel.pkl')
    
    return dictMerged


def Regression(date,dict_df_ret,dict_df_fexpo,dict_date_map):
    dateadd=dict_date_map[date]
    Y=dict_df_ret[dateadd]

    #Y.dropna(inplace=True)
    
    #if Y.empty == True:
        #return None
    
    X=dict_df_fexpo[date]
    model = sm.OLS(Y, X)
    results = model.fit()
    df_model_params=pd.DataFrame(results.params,columns=['params'])
    df_model_resid=pd.DataFrame(results.resid,columns=['resid'])
    return {'params':df_model_params,'resid':df_model_resid}
    
def calcfactorRetCov(panel_factorretcov,date,allfactor):   
    df_onedate=panel_factorretcov.T[date]                  
    df_onedate['factorid1']=df_onedate.index
    df_l_factorretcov = pd.melt(df_onedate,id_vars=['factorid1'],value_vars=allfactor)
    df_l_factorretcov['date']=date
    df_l_factorretcov['factorid1']=list(gftIO.strSet2Np(np.array(df_l_factorretcov['factorid1'])))
    df_l_factorretcov['variable']=list(gftIO.strSet2Np(np.array(df_l_factorretcov['variable'])))
    return df_l_factorretcov

def fexpomerge(dict_risk_expo_new,date,allfactor,ls_allsymbols):
    ls_raw_df_fexpo=[dict_risk_expo_new[factorname].reindex(index=[date],columns=ls_allsymbols[date]).rename(index={date:factorname}) for factorname in allfactor] 
    df_fexpo_onedate=pd.concat(ls_raw_df_fexpo,axis=0).T.fillna(0)
    return df_fexpo_onedate
