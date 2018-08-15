# <codecell>

import numpy as np
import pandas as pd
from functools import reduce
import math as mt

import statsmodels.api as sm
from lib.gftTools import gftIO
import datetime

#x0 = gftIO.zload("x0.pkl")

#x1 = gftIO.zload("x1.pkl")
#x2 = gftIO.zload("x2.pkl")


##import pickle 
##pickle.dump(x0, open( "x0.pkl", "wb" ))

def riskModel(df_ret,dict_risk_expo,weight,corrhalflife,varhalflife):
    '''
    df_ret=x0
    dict_risk_expo=x1
    weight=x2
    corrhalflife=x3
    varhalflife=x4
    '''
    ls_fexponame=list(map(gftIO.gidInt2Str,list(dict_risk_expo['osets'].asColumnTab()['O0'])))
    
    ind_factor_name=sorted(list(map(gftIO.gidInt2Str,list(dict_risk_expo[ls_fexponame[0]].asColumnTab()['O0']))))
    sty_factor_name=sorted(list(map(gftIO.gidInt2Str,list(dict_risk_expo[ls_fexponame[1]].asColumnTab()['O0']))))
    allfactor =ind_factor_name +sty_factor_name
        
    
    ##stock return preprocess
    df_w_ret=df_ret.asMatrix().T.dropna(how='all',axis=1)
    
    ##factor exposure preprocess
    dict_risk_expo_new = {factorname: dict_risk_expo[factorname].asMatrix().dropna(how='all') for factorname in allfactor}
    ls_ls_fexpodate=list([dict_risk_expo_new[factorname].index.tolist() for factorname in dict_risk_expo_new.keys()]) 
    ls_alldates_fexpo=reduce(np.intersect1d,ls_ls_fexpodate)
    
    ls_ls_fexposymbol=list([dict_risk_expo_new[factorname].columns.tolist() for factorname in dict_risk_expo_new.keys()]) 
    ls_allsymbols_fexpo=reduce(np.intersect1d,ls_ls_fexposymbol)
    
    ##weight preprocess
    weight=weight.asMatrix().T
        
    ##get the date/symbol intersection of (stock return,factor exposure,weight)
    
    ##ls_alldates save the stock return map date
    
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
    
    
    ls_alldates = sorted(list(set(weight.columns).intersection(set(df_w_ret.columns)).intersection(set(dict_date_map.values()))))
    ls_alldates_ondaybefore=sorted(list(dict_date_map.keys()))
    ls_allsymbols={date: list(set(df_w_ret[[dict_date_map[date]]].dropna().index).intersection(set(ls_allsymbols_fexpo)).intersection(set(weight.index))) for date in ls_alldates_ondaybefore}
    
    
    ##align the stock return and factor exposure
    dict_df_weight_raw={date:weight[[date]].reindex(index=ls_allsymbols[date]).fillna(0) for date in ls_alldates_ondaybefore}
    dict_df_weight={date:np.sqrt(dict_df_weight_raw[date]) for date in ls_alldates_ondaybefore}
    
    dict_df_ret={dict_date_map[date]: pd.concat([(df_w_ret[[dict_date_map[date]]].reindex(index=ls_allsymbols[date])) * (dict_df_weight[date].rename(columns={date:dict_date_map[date]})),pd.DataFrame(data=np.zeros(1),index=['constrain'],columns=[dict_date_map[date]])],axis=0) for date in ls_alldates_ondaybefore}
    dict_df_fexpo_raw ={date:fexpomerge(dict_risk_expo_new,date,allfactor,ls_allsymbols) for date in ls_alldates_ondaybefore}  
    dict_df_fexpo ={date:dict_df_fexpo_raw[date].assign(countryfactor=1).multiply(dict_df_weight[date].squeeze(),axis='index') for date in ls_alldates_ondaybefore} 



    ##calculate constraints
    dict_df_fexpo_con ={date:expoconstrain(dict_df_fexpo_raw,date,ind_factor_name,allfactor,dict_df_weight_raw,sty_factor_name,dict_df_fexpo) for date in ls_alldates_ondaybefore} 
    

    #for i in dict_risk_expo_new.keys():
        #if dict_risk_expo_new[i].index.min() > df_l_ret.index.min() or dict_risk_expo_new[i].index.max() < df_l_ret.index.max():
            #raise Exception
            
    
    ########################step3:calculate factor return########################
    
    ls_df_fitresult={dict_date_map[date]:Regression(date,dict_df_ret,dict_df_fexpo_con,dict_df_weight,dict_df_fexpo,dict_date_map) for date in ls_alldates_ondaybefore}
    
    ls_df_facreturn=list(ls_df_fitresult[date]['params'].rename(columns={'params':date}) for date in ls_alldates)
    df_model_params=reduce(lambda df_para1,df_para2:pd.concat([df_para1,df_para2],axis=1),ls_df_facreturn)
    
    ########################step4:calculate factor return covariance########################  
    
    df_allfactorret=df_model_params.T
    df_allfactorret=df_allfactorret.sort_index()
    
    corrhalflife=int(corrhalflife)
    varhalflife=int(varhalflife)
    
    halflife = max(corrhalflife, varhalflife)
     
    if len(ls_alldates) < halflife:
        raise Exception("More data needed")
    else:
        ls_alldatesnew=ls_alldates[halflife-1:len(ls_alldates)]
        corrwgts=list(map(lambda x:mt.sqrt(0.5**(x/int(corrhalflife))),list(range(int(corrhalflife)-1,-1,-1))))
        varwgts=list(map(lambda x:mt.sqrt(0.5**(x/int(varhalflife))),list(range(int(varhalflife)-1,-1,-1))))
        
        ls_factorretcov=list(calcfactorRetCov(df_allfactorret,date,corrwgts,varwgts,corrhalflife,varhalflife) for date in ls_alldatesnew)
        df_l_factorretcov=pd.concat(ls_factorretcov,axis=0).rename(columns={'variable':'factorid2'})

                                  
    ########################step5:calculate the residual(specific) variances of regression########################
    
    ##part1:merge factorreturn,factor exposure and stock return
        ls_specificrisk=list(ls_df_fitresult[date]['resid'].rename(columns={'resid':date}) for date in ls_alldates)
        df_w_specificrisk=pd.concat(ls_specificrisk,axis=1).T
        df_w_specificrisk=df_w_specificrisk.sort_index()
        specificwgts=list(map(lambda x:mt.sqrt(0.5**(x/int(halflife))),list(range(int(halflife)-1,-1,-1))))
    
        ls_factorretspe=list(calcfactorRetSpe(df_w_specificrisk,date,specificwgts,halflife) for date in ls_alldatesnew)
        df_specificrisk_var=pd.concat(ls_factorretspe,axis=0)

    ########################step6:generate final return value########################
        df_allfactorret=df_allfactorret.drop('countryfactor',axis=1)
        dict_factorret={key+'.ret': df_allfactorret[[key]].rename(columns={key:list(gftIO.strSet2Np(np.array(list(df_allfactorret[[key]].columns))))[0]}) for key in df_allfactorret.columns}
        dictMerged=dict(dict_factorret, **dict_risk_expo, **{'ret_cov':df_l_factorretcov,'specificRisk':df_specificrisk_var})                       
        return dictMerged

def Regression(date,dict_df_ret,dict_df_fexpo_con,dict_df_weight,dict_df_fexpo,dict_date_map):
    dateadd=dict_date_map[date]
    
    Y=np.array(dict_df_ret[dateadd][dateadd])
    X=np.array(dict_df_fexpo_con[date])
    
    model = sm.RLM(Y,X,M=sm.robust.norms.HuberT())   
    results = model.fit()
    df_model_params=pd.DataFrame(results.params,columns=['params'])
    df_model_params.index=dict_df_fexpo_con[date].columns
                                           
    df_model_params=df_model_params.ix[0:37,]
    df_model_resid=pd.DataFrame(results.resid,columns=['resid'])
    df_model_resid.index=dict_df_fexpo_con[date].index
    df_model_resid=df_model_resid.reindex(dict_df_fexpo[date].index)
    df_model_resid=df_model_resid.multiply(1/dict_df_weight[date].squeeze(),axis='index') 
    
    return {'params':df_model_params,'resid':df_model_resid}

def calcfactorRetCov(df_allfactorret,date,corrwgts,varwgts,corrhalflife,varhalflife):
    ##calculate corr
    df_factorretcorr = df_allfactorret[df_allfactorret.index <= date][-corrhalflife:]
    df_retcorr=df_factorretcorr.apply(lambda x: np.array(x) * np.array(corrwgts)).corr()
    ##calculate standard deviation
    df_factorretstd = df_allfactorret[df_allfactorret.index <= date][-varhalflife:]
    df_retstd=df_factorretstd.apply(lambda x: np.array(x) * np.array(varwgts)).std()
    ##calculate covariance
    df_retcov=df_retcorr.apply(lambda x: np.array(x) * np.array(df_retstd)).T.apply(lambda x: np.array(x) * np.array(df_retstd))
    
    df_retcov['factorid1']=df_retcov.index
    df_l_factorretcov = pd.melt(df_retcov,id_vars=['factorid1'])
    df_l_factorretcov['date']=date
    
    ssb_map=pd.DataFrame(data=list(set(df_l_factorretcov['factorid1'][df_l_factorretcov['factorid1'] != 'countryfactor'])),columns=['oriname'])
    ssb_map=ssb_map[ssb_map['oriname'] != 'countryfactor']
    ssb_map['sname']=list(gftIO.strSet2Np(np.array(ssb_map['oriname'])))
    dict_ssb_map={key:list(ssb_map['sname'][ssb_map['oriname'] == key])[0] for key in ssb_map['oriname']}
    dict_ssb_map['countryfactor'] = 'countryfactor'
    
    df_l_factorretcov['factorid1']=df_l_factorretcov['factorid1'].apply(lambda x:dict_ssb_map[x])
    df_l_factorretcov['variable']=df_l_factorretcov['variable'].apply(lambda x:dict_ssb_map[x])
    df_l_factorretcov=df_l_factorretcov[df_l_factorretcov['factorid1'] != 'countryfactor'][df_l_factorretcov['variable'] != 'countryfactor']
    
    return df_l_factorretcov

def calcfactorRetSpe(df_w_specificrisk,date,specificwgts,halflife):
    df_residualspe = df_w_specificrisk[df_w_specificrisk.index <= date][-halflife:]
    df_retspe=df_residualspe.apply(lambda x: np.array(x) * np.array(specificwgts)).var()
    df_retspenew=pd.DataFrame(df_retspe,columns=['specificrisk'])
    df_retspenew['symbol'] = df_retspenew.index
    df_retspenew=df_retspenew.reset_index().assign(date=date).drop('index',axis=1) 
    
    return df_retspenew

def fexpomerge(dict_risk_expo_new,date,allfactor,ls_allsymbols):
    ls_raw_df_fexpo=[dict_risk_expo_new[factorname].reindex(index=[date],columns=ls_allsymbols[date]).rename(index={date:factorname}) for factorname in allfactor] 
    df_fexpo_onedate=pd.concat(ls_raw_df_fexpo,axis=0).T.fillna(0)
    return df_fexpo_onedate


def expoconstrain(dict_df_fexpo_raw,date,ind_factor_name,allfactor,dict_df_weight_raw,sty_factor_name,dict_df_fexpo):
    df_fexpo_date=dict_df_fexpo_raw[date].reindex(columns=ind_factor_name).multiply(dict_df_weight_raw[date].squeeze(),axis='index')
    df_wgt_con=pd.DataFrame(df_fexpo_date.sum(axis=0)).T.rename(index={0:'constrain'})
                           
    df_con_add=pd.DataFrame((np.zeros([1,len(allfactor)-len(ind_factor_name)])),index=['constrain'],columns=sty_factor_name)
    df_wgt_con_fnl=pd.concat([df_wgt_con,df_con_add],axis=1)
    return pd.concat([dict_df_fexpo[date],df_wgt_con_fnl.assign(countryfactor=0)],axis=0)

# <codecell>



# <codecell>


