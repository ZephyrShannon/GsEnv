# <codecell>

import numpy as np
import pandas as pd



# <codecell>

def ARCH_test(context,y,x):
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
         
        # obtain p value of Breusch Goldfrey LM test (return 4 list of name and value)
        ARCH_test = ARCH(x_array,y_array)[3][1]
        # set significant level for Breusch Goldfrey LM test
        alpha = 0.05
        
        if  ARCH_test < alpha:
            autocorrelation[i] = True
    
    if any(i == True for i in autocorrelation):
        autocorr_fix = '8C44697086A1456CB9C54FF68AB8210A'
        return autocorr_fix
    else:
        return '0F6C84D05AFE11E3949A0800200C9A66'



	

# <codecell>

# OLS fit
def ols(x,y):
    ols_model=sm.OLS(y,x)    
    return ols_model.fit()

# <codecell>

# Engle’s Test for Autoregressive Conditional Heteroscedasticity (ARCH): 
# (AR(p)): ep_t**2 = a_0 + a_1 ep_t-1**2 + ..+ a_p ep_t-p **2 +  e_t
# check time series error variance depends on previous time periods' error terms 
# null: variance do not depend on previous errors
def ARCH(x,y):
    ols_retults=ols(x,y)
    name = ['LM statistic', 'p-value of LM test', 
            'f-statistic of the hypothesis', 'f p-value']
    test = sms.het_arch(ols_results.resid)
    return lzip(name,test)


# <codecell>

