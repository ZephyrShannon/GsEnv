# <codecell>


import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.stats.api as sms



# <codecell>

# !! Currently assume input is dataframe and will perform remedy for all data when even only one time series under a stock was detected as autocorrelation

# DW test not valid when all errors are zeros

def Autocorrelation_AR_1_test(context,y,x):
    # axis =1: check on time series
    
    # y is a preprocessed stock return (DataFrame) with dates as index and symbols as Column 
    y_df = y.asMatrix()
    date_ls = list(y_df.index)
    symbol_ls = list(y_df.columns)
    y_series = pd.Series()

    # x is a preprocessed selected factor exposure (Dictionary and DataFrame), \
    # with factor name as keys and dataframe where index-dates and columns-symbols as values \
    # ( !!! dates and symbols are equal to those of y's)
    x_dic = x
    factor_ls = list(x_dic.keys())
    
        
    autocorrelation=[None]*len(symbol_ls)
    
    for i in range(len(y_df.columns)):
        x_ls = []
        y_series = y_df.iloc[:,i]
        for value in x_dic.values():
            x_df = value.asMatrix().iloc[:,i]
            x_ls.append(x_df)
        x_df = pd.concat(x_ls,axis=1,ignore_index=True)
        x_array = x_df.fillna(0).as_matrix(columns=None)
        y_array = y_series.fillna(0).as_matrix(columns=None)
        
        
        # obtain DW test statistic d
        DW_test = Durbin_Watson(x_array,y_array)
        # set the distance of d from 2
        DW_distance = 1 
        
        if  abs(DW_test-2)>=DW_distance:
            autocorrelation[i] = True
    
    
    if any(i == True for i in autocorrelation):
        autocorr_fix = '2C0673FC1B6C4C979E9800DEE1C70E8B'
        return autocorr_fix
    else:
        return '0F6C84D05AFE11E3949A0800200C9A66'
    

# <codecell>

#OLS fit
def ols(x,y):
    ols_model=sm.OLS(y,x)
    ols_results = ols_model.fit()
    return ols_results

# <codecell>

#2. Durbin-Watson test
# d= sum(e_t -e_t-1)**2 / sum(e_t)**2
# 0<=d<=4, no correlation if the result is close to 2

def Durbin_Watson(x,y):
    ols_results=ols(x,y)
    resid = ols_results.resid
    test = sms.stattools.durbin_watson(resid,axis=0)
    return test

# <codecell>

