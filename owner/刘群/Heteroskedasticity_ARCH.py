# <codecell>

import numpy as np
import pandas as pd
from arch import arch_model


# <codecell>

def Heteroskedasticity_ARCH(context,y,x):
    # axis =1: check on time series (for each stock)
    
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
    arch_ls=[None]*len(symbol_ls)
    
    for i in range(len(symbol_ls)):
        x_ls = []
        y_series = y_df.iloc[:,i]
        for value in x_dic.values():
            x_df = value.asMatrix().iloc[:,i]
            x_ls.append(x_df)
        x_df = pd.concat(x_ls,axis=1,ignore_index=True)
        x_array = x_df.fillna(0).as_matrix(columns=None)
        y_array = y_series.fillna(0).as_matrix(columns=None)    
        
        # ARCH model as r=mu + epsilon, sigma^2 = omega + alpha * epsilon^2 + beta * sigma^2
        # univariate, turn off display of 'summary' to get coefficients
        am = arch_model(y,x).fit(disp = 'off')
        
        # set output as parameter mu
        arch_ls[i] = am.iloc[0]
    
    return arch_ls
    

    



	

# <codecell>

