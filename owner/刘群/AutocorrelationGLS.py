# <codecell>

import numpy as np
import pandas as pd



# <codecell>

def AutocorrelationGLS(context,y,x):
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

    # Creat beta DataFrame
    beta = pd.DataFrame(np.zeros((len(symbol_ls),len(factor_ls))),columns=factor_ls)
    
    for i in range(len(y_df.columns)):
        x_ls = []
        y_series = y_df.iloc[:,i]
        for value in x_dic.values():
            x_df = value.asMatrix().iloc[:,i]
            x_ls.append(x_df)
        x_df = pd.concat(x_ls,axis=1,ignore_index=True)
        x_array = x_df.fillna(0).as_matrix(columns=None)
        y_array = y_series.fillna(0).as_matrix(columns=None)
        
        newy_west = newey_west(x,y)
        # featured generalised least square estimated coefficients
        beta.iloc[i] = newy_west.params()
    return beta

	

# <codecell>

## Autocorrelation fix
# Using Newey-West estimator to estimate covariance matrix (lag=1)
# Also shows Durbin-Watson test
# small sample correction??
def newey_west(x,y):
    ols_retults=ols(x,y)
    FGLS = ols_results.get_robustcov_results(cov_type='HAC',maxlags=999)
    return FGLS

# <codecell>

#OLS fit
def ols(x,y):
    ols_model=sm.OLS(y,x)
    ols_results = ols_model.fit()
    return ols_results

# <codecell>

