# <codecell>

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.stats.api as sms
from statsmodels.compat import lzip
import statsmodels.stats.outliers_influence as smo


# <codecell>

# If matrix x is singular, the test of Breusch Goldfrey would fail, so one may would like to perform multicollinearity detection and remedy first


def AutocorrelationDetection(context,y,x):
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
        
        # obtain p value of Breusch Goldfrey LM test 
        BG_test = Breusch_Goldfrey(x_array,y_array)[3][1]
        # set significant level for Breusch Goldfrey LM test
        alpha = 0.05
        
        # obtain DW test statistic d
        DW_test = Durbin_Watson(x_array,y_array)
        # set the distance of d from 2
        DW_distance = 1 
        
        if  BG_test < alpha or abs(DW_test-2)>=DW_distance:
            autocorrelation[i] = True
            
    if any(i == True for i in autocorrelation):
        autocorr_fix = 'E8BB8D4B79E14D2E9FF12A80F7605F70'
        return autocorr_fix
    else:
        return '0F6C84D05AFE11E3949A0800200C9A66'
    



# <codecell>

# OLS fit
def ols(x,y):
    ols_model=sm.OLS(y,x)    
    return ols_model.fit()

# <codecell>

# 1. Breusch-Godfrey LM test (AR(p)) : 
# ep_t = del_0 + del_1 x_t,1 + del2 x_t,2+...a_1 ep_t-1 +...+ a_p ep_t-p +e_t
# check redisuals in regression
# null: errors do not depends on previous errors of order up to p=1

def Breusch_Goldfrey(x,y):
    ols_results=ols(x,y)
    name = ['LM statistic', 'p-value of LM test', 
            'f-statistic of the hypothesis', 'f p-value']
    test = sms.acorr_breusch_godfrey(ols_results)
    return lzip(name,test)

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

