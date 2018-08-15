# <codecell>

import numpy as np
import pandas as pd
import xarray
import math as mt
def calc_factor_ret_cov(context,df_factor_ret,corr_half_life,var_half_life):
    '''
    Input: 
        context:
        df_factor_ret: dict,{'param':xarray of daily factor return, 'resid':xarray of ...}
        corr_half_life: int
        var_half_lifr: int
    
    ----------
    Pseudo code:
    core:
        $cov(f_i,f_j)=\rho_{i,f} \sigma_i \sigma_j
        s1.to get the cov mat at day K
            0. slice the data
            
            1. \rho_{i,j}:
                get corr mat, modified by corr_half_life
            2. \sigma_i:
                get sd vector, modified by var_half_life
                
            3. cov(f_i,f_j)=\rho_{i,f} \sigma_i \sigma_j, 
                
        s2. return a dict of {timestamps: cov mat},
            where cov mat is df whose columns and index are factor names
    ----------
    
    '''
    # data preprocessing 
    # from xarray to df, index= timestamps, colunms= factor names
    
    #get df of factor return, date list and factor names list
    #df_factor_ret=pd.DataFrame(np.array( df_factor_ret['param']), 
            #                   index=list(df_factor_ret['param'].date.values),
               #                columns=list(df_factor_ret['param'].factors.values))
            
    df_factor_ret=df_factor_ret.asMatrix()
    ls_date = df_factor_ret.index.tolist()       ##date list
    # ls_fac_name = df_factor_ret.columns.tolist() ##fac_name list
    
    
    halflife = max(corr_half_life, var_half_life)
       
    # raise exception
    if len(ls_date) < halflife:
        raise Exception("More data needed")
    else:
        ls_date_for_loop = ls_date[halflife-1:len(ls_date)]
        
    # cal. corr and var weights list
    corrwgts = list(
                map(
                        lambda x:mt.sqrt(0.5**(x/int(corr_half_life))),  ## \sqrt{0.5^{x/corrhalf=4}}
                        list(range(int(corr_half_life)-1, -1, -1)) ) )
    varwgts = list(
                map(
                        lambda x:mt.sqrt(0.5**(x/int(var_half_life))),    ## \sqrt{0.5^{x/varhalf=5}}
                        list(range(int(var_half_life)-1,-1,-1)) ) )

    
    
    #get a dict of cov matrix, key=timestamp, value=cov mat#

    dict_retcov={}
    for date in ls_date_for_loop:
        # s1.0
        df_factorretcorr = df_factor_ret[df_factor_ret.index <= date][-corr_half_life:]

        df_factorretstd = df_factor_ret[df_factor_ret.index <= date][-var_half_life:]

        # s1.1
        df_retcorr=df_factorretcorr.apply(lambda x: np.array(x) * np.array(corrwgts)).corr()      

        # s1.2 calculate standard deviation        
        df_retstd=df_factorretstd.apply(lambda x: np.array(x) * np.array(varwgts)).std()

        
        # s1.3 calculate covariance
        df_retcov = df_retcorr.apply(
                lambda x: np.array(x) * np.array(df_retstd)).T.apply(
                        lambda x: np.array(x) * np.array(df_retstd))
        
        dict_retcov[date]=df_retcov 
    ######################################################

    # s2
    return dict_retcov
