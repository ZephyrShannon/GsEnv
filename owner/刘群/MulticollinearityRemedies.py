# <codecell>

import numpy as np
import pandas as pd


def MulticollinearityRemedies(y,x,precheck):
    # Assume y is a preprocessed stock return (DataFrame) with dates as index and symbols as Column 
    y_df = y.asMatrix()
    y_series = pd.Series()

    # Assume x is a preprocessed selected factor exposure (Dictionary and DataFrame), \
    # with factor name as keys and dataframe where index-dates and columns-symbols as values \
    # ( !!! dates and symbols are equal to those of y's)
    x_dic = x
    x_ls = []
    
    # if input is 0, build regression on time series for each symbol
    if precheck['axis']==0:
        print("Precheck on time series model for each stock")
        for i in range(len(y_df.columns)):
            y_series = y_df.iloc[:,i]
            for value in x_dic.values():
                x_df = value.asMatrix().iloc[:,i]
                x_ls.append(x_df)
            x_df = pd.concat(x_ls,axis=1,ignore_index=True)
            x_array = x_df.fillna(0).as_matrix(columns=None)
            y_array = y_series.fillna(0).as_matrix(columns=None)
            return print(ols_remedy(x_array,y_array))
    
    # if input is 1, build regression on all symbols for each date
    if precheck['axis']==1:
        print("Precheck on stock returns for each date")
        for i in range(len(y_df.index)):
            y_series = y_df.iloc[i]
            for value in x_dic.values():
                x_df = value.asMatrix().iloc[i]
                x_ls.append(x_df)
            x_df = pd.concat(x_ls,axis=1,ignore_index=True)
            x_array = x_df.fillna(0).as_matrix(columns=None)
            y_array = y_series.fillna(0).as_matrix(columns=None)
            return print(ols_remedy(x_array,y_array)) 

# <codecell>

def ols_remedy(x,y):
    remedy={'Lasso Regression': lasso_reg(x,y),'Ridge Regression': ridge_reg(x,y),'ElasticNet Regression':elasticnet_reg(x,y)}
    return remedy

# <codecell>

# 1. Lasso Regression
from sklearn.linear_model import LassoCV
# lassoCV() defalut: 
# alphas =None: set alpha automatically
# fit_intercept=True
# cv=None: 3-fold cross-validation 
def lasso_reg(x,y):
    alpha = np.logspace(-2,10,num=50)
    lassocv = LassoCV(alphas = alpha, cv=20)
    lassocv.fit(x, y)
    lassocv_score = lassocv.score(x, y)
    lassocv_alpha = lassocv.alpha_
    print('Lasso R square', lassocv_score)
    print('Lasso Alpha', lassocv_score )
    return lassocv.coef_

# <codecell>

# 2. Ridge Regression
from sklearn.linear_model import RidgeCV
# alphas=(0.1, 1.0, 10.0)
# fit_intercept=True
# cv=None: to use the efficient Leave-One-Out cross-validation
# cv=int: to specify the number of folds
def ridge_reg(x,y):
    ridgecv = RidgeCV(alphas=(0.1,10,50),cv=20)
    ridgecv.fit(x, y)
    ridgecv_score = ridgecv.score(x, y)
    ridgecv_alpha = ridgecv.alpha_
    print('Ridge R square', ridgecv_score)
    print('Ridge Alpha', ridgecv_alpha )
    return ridgecv.coef_

# <codecell>

# 3. ElasticNet Regression
from sklearn.linear_model import ElasticNetCV
# l1_ratio=0.5 : closer to 1 means more weight on lasso l1
# alphas =None: set alpha automatically
# fit_intercept=True
# cv=None: 3-fold cross-validation 
def elasticnet_reg(x,y):
    elasticnetcv = ElasticNetCV(cv=20)
    elasticnetcv.fit(x, y)
    elasticnetcv_score = elasticnetcv.score(x, y)
    elasticnetcv_alpha = elasticnetcv.alpha_
    print('ElasticNet R square', elasticnetcv_score)
    print('ElasticNet Alpha', elasticnetcv_alpha )
    return elasticnetcv.coef_
