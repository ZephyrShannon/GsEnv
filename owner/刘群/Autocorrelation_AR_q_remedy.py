# <codecell>

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.stats.api as sms
from statsmodels.compat import lzip
import statsmodels.stats.outliers_influence as smo


# <codecell>

def Autocorrelation_AR_q_remedy(context,y,x):
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
        
        beta.iloc[i] = Newey_West(x_array,y_array)
        
    return print(beta)

	

# <codecell>

# OLS fit
def ols(x,y):
    ols_model=sm.OLS(y,x)    
    return ols_model.fit()

# <codecell>

def Newey_West(x,y):
    ols_results=ols(x,y)
    FGLS = ols_results.get_robustcov_results(cov_type='HAC',maxlags=999)
    return FGLS.params

# <codecell>

