# <codecell>

import numpy as np
import pandas as pd


# if input is 1, build regression on time series for each symbol;\
# if input is 0, build regression on all symbols for each date

def MulticollinearityDetection(axis,x,y):
    # Assume y is a preprocessed stock return (DataFrame) with dates as index and symbols as Column 
    y_df = y.asMatrix()
    date_ls = list(y_df.index)
    symbol_ls = list(y_df.columns)
    y_series = pd.Series()

    # Assume x is a preprocessed selected factor exposure (Dictionary and DataFrame), \
    # with factor name as keys and dataframe where index-dates and columns-symbols as values \
    # ( !!! dates and symbols are equal to those of y's)
    x_dic = x
    factor_ls = list(x_dic.keys())
    
    
    if axis==1:
        
        multicollinearity=[None]*len(symbol_ls)
        print("Precheck on time series model for each stock")
        for i in range(len(y_df.columns)):
            x_ls = []
            y_series = y_df.iloc[:,i]
            for value in x_dic.values():
                x_df = value.asMatrix().iloc[:,i]
                x_ls.append(x_df)
            x_df = pd.concat(x_ls,axis=1,ignore_index=True)
            x_array = x_df.fillna(0).as_matrix(columns=None)
            y_array = y_series.fillna(0).as_matrix(columns=None)
            precheck_dic =ols_precheck(x_array,y_array)
            # print(precheck_dic)
            if any(j>=10 for j in precheck_dic['VIF'].iloc[:,0].tolist()) or precheck_dic['Conditional Number']>=30:
                multicollinearity[i] = True
        if any(i == True for i in multicollinearity):
            ridge = '22D34826DF0D4114B197E6329F4F0C63'
            return ridge
        else:
            return '0F6C84D05AFE11E3949A0800200C9A66'
        
    
    if axis==0:

        multicollinearity = [None]*len(date_ls)
        print("Precheck on stock returns for each date")
        for i in range(len(y_df.index)):
            x_ls = []
            y_series = y_df.iloc[i]
            for value in x_dic.values():
                x_df = value.asMatrix().iloc[i]
                x_ls.append(x_df)
            x_df = pd.concat(x_ls,axis=1,ignore_index=True)
            x_array = x_df.fillna(0).as_matrix(columns=None)
            y_array = y_series.fillna(0).as_matrix(columns=None)
            precheck_dic =ols_precheck(x_array,y_array)
            # print(precheck_dic)
            if any(j>=10 for j in precheck_dic['VIF'].iloc[:,0].tolist()) or precheck_dic['Conditional Number']>=30:
                multicollinearity[i] = True
        if any(i == True for i in multicollinearity):
            ridge ='01C56B6A73FD4A098A864F08A18F861D'
            return ridge
        else:
            return '0F6C84D05AFE11E3949A0800200C9A66'

# <codecell>

import statsmodels.api as sm
def ols_precheck(x,y):
    precheck={'OLS Summary':ols_summary(x,y),'VIF':VIF(sm.add_constant(x)),'Conditional Number':Cond_No(x)}
    return precheck

# <codecell>

# OLS fit
def ols(x,y):
    ols_model=sm.OLS(y,x)    
    return ols_model.fit()

# OLS summary
def ols_summary(x,y):
    ols_results = ols(x,y)
    return ols_results.summary()


# <codecell>

#1. VIF: there is highly collinearity if it is above 5 or 10
import statsmodels.stats.outliers_influence as smo
def VIF(x):
    vif=pd.DataFrame()
    vif["VIF Factor"]=[smo.variance_inflation_factor(x, i) for i in range(x.shape[1])]
    return vif

# <codecell>

#2. Condition Number Test: there is highly collinearity if it is above 30
def Cond_No(x):
    cond=np.linalg.cond(np.dot(x.T,x))
    return cond
