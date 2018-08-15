# <codecell>

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.stats.api as sms
from statsmodels.compat import lzip
import statsmodels.stats.outliers_influence as smo


# <codecell>

def Autocorrelation_AR_1_Remedy(context,y,x):
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
    
        
    beta = pd.DataFrame(np.zeros((len(symbol_ls),len(factor_ls))),index = symbol_ls, columns = factor_ls)
    
    for i in range(len(symbol_ls)):
        x_ls = []
        y_series = y_df.iloc[:,i]
        for value in x_dic.values():
            x_df = value.asMatrix().iloc[:,i]
            x_ls.append(x_df)
        x_df = pd.concat(x_ls,axis=1,ignore_index=True)
        x_array = x_df.fillna(0).as_matrix(columns=None)
        y_array = y_series.fillna(0).as_matrix(columns=None)
        
        beta.iloc[i] = cochrane_orcutt(x_array,y_array)
        
    return print(beta)

	

# <codecell>

#OLS fit
def ols(x,y):
    ols_model=sm.OLS(y,x)
    ols_results = ols_model.fit()
    return ols_results

# <codecell>

# Durbin-Watson test
# d= sum(e_t -e_t-1)**2 / sum(e_t)**2
# 0<=d<=4, no correlation if the result is close to 2

def Durbin_Watson(resid):
    test = sms.stattools.durbin_watson(resid,axis=0)
    return test

# <codecell>

# Cochrane_Orcutt Procedure - AR(1) Correction
def cochrane_orcutt(x,y):

    max_iter = 100

    resid = ols(x,y).resid
    
    for i in range(max_iter):
        resid_lag_1 = resid[0:len(resid)-1]
        rho = ols(resid_lag_1,resid[1:len(resid)]).params
        y_new = y[1:len(y)]-rho*y[0:len(y)-1]
        x_new = x[1:x.shape[0],:]-rho*x[0:x.shape[0]-1,:]
        beta = ols(x_new,y_new).params
        beta[0] = beta[0]/(1-rho)
        
        resid = y - np.dot(x,beta)
        
        # obtain DW test statistic 0<=d<=4
        DW_test = Durbin_Watson(resid)
        # set the distance of d from 2
        DW_distance = 1  
        if  abs(DW_test-2)>=DW_distance:
            continue
        else:
            break
    

    return beta

# <codecell>

