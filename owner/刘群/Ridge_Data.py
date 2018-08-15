# <codecell>

import numpy as np
import pandas as pd


# Assume x,y are arrays
def Ridge_Data(context,x,y):
    x,y = data_process(x,y)
    # standardize independent variables and response variable (necessary for ridge regularization)
    from sklearn.preprocessing import StandardScaler
    x_std = StandardScaler().fit_transform(x)
    y_std = StandardScaler().fit_transform(y.reshape(-1,1))
    
    
    # Ridge Regression RidgeCV() default:
    # alphas=(0.1, 1.0, 10.0)
    # fit_intercept=True
    # cv=None: to use the efficient Leave-One-Out cross-validation
    # cv=int: to specify the number of folds
    from sklearn.linear_model import RidgeCV
    ridgecv = RidgeCV()
    ridgecv.fit(x_std, y_std)
    ridgecv_score = ridgecv.score(x_std, y_std)
    # ridge panelty: alpha
    ridgecv_alpha = ridgecv.alpha_
    
    print('Ridge R square', ridgecv_score)
    print('Ridge Alpha', ridgecv_alpha )
    print('Ridge Coefficients',ridgecv.coef_)

    # Estimated coefficients are the same!!
    import math
    k = len(x_std[0])
    y_ridge = np.append(y_std,np.zeros(k))
    x_ridge = np.append(x_std,np.identity(k)*math.sqrt(ridgecv_alpha),axis=0)

# <codecell>

def data_process(x,y)    
    
    # Assume y is a preprocessed stock return (DataFrame) with dates as index and symbols as Column 
    y_df = y.asMatrix()
    y_series = pd.Series()

    # Assume x is a preprocessed selected factor exposure (Dictionary and DataFrame), \
    # with factor name as keys and dataframe where index-dates and columns-symbols as values \
    # ( !!!???? dates and symbols are equal to those of y's)
    x_dic = x
    x_ls = []
    

    # print("Precheck on time series model for each stock")
        for i in range(len(y_df.columns)):
            y_series = y_df.iloc[:,i]
            for value in x_dic.values():
                x_df = value.asMatrix().iloc[:,i]
                x_ls.append(x_df)
            x_df = pd.concat(x_ls,axis=1,ignore_index=True)
            x_array = x_df.fillna(0).as_matrix(columns=None)
            y_array = y_series.fillna(0).as_matrix(columns=None)
            precheck_dic =ols_precheck(x_array,y_array)
            print(precheck_dic)
            if any(j>=10 for j in precheck_dic['VIF'].tolist()) or precheck_dic['Conditional Number']>=30:
                ridge ='911E8AD6683D43CE8574A09C142142D8'
                return ridge
            else:
                return None_GID
        
    
    
