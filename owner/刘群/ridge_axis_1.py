# <codecell>

import numpy as np
import pandas as pd
import copy
    
    # build regression on all symbols for each date
def ridge_axis_1(context,x,y):

    # Assume y is a preprocessed stock return (DataFrame) with dates as index and symbols as Column 
    y_df = y.asMatrix()
    y_series = pd.Series()
    date_ls = list(y_df.index)
    symbol_ls = list(y_df.columns)


    # Assume x is a preprocessed selected factor exposure (Dictionary and DataFrame), \
    # with factor name as keys and dataframe where index-dates and columns-symbols as values \
    # ( !!! dates and symbols are exactly the same as those of y's)
    x_dic = x

    factor_ls = list(x_dic.keys())

    # Assign new data
    add_y = pd.DataFrame(np.zeros((len(date_ls),len(factor_ls))),index = date_ls)
    add_x = add_y
    
    y_df_new = pd.concat([y_df,add_y],axis=1)
    
    x_dic_new =copy.deepcopy(x_dic)    
    for key,value in x_dic_new.items():
        new_value = value.asMatrix()
        new_value = pd.concat([new_value, add_x],axis=1)
        x_dic_new[key] = new_value     
    
    # Creat beta DataFrame
    ridge_df = pd.DataFrame(np.zeros((len(date_ls),len(factor_ls))),columns=factor_ls)
  

    for i in range(len(date_ls)):
        
        y_series = y_df.iloc[i]
        
        x_dic_iter =copy.deepcopy(x_dic)
        x_ls = []
        
        for value in x_dic_iter.values():
            x_df = value.asMatrix().iloc[i]
            x_ls.append(x_df)
        x_df = pd.concat(x_ls,axis=1,ignore_index=True)
        x_array = x_df.fillna(0).as_matrix(columns=None)
        y_array = y_series.fillna(0).as_matrix(columns=None)
 
        # standardize independent variables and response variable (necessary for ridge regularization)
        from sklearn.preprocessing import StandardScaler
        x_std = StandardScaler().fit_transform(x_array)
        y_std = StandardScaler().fit_transform(y_array.reshape(-1,1))


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
        # ridge estimated coefficients
        ridgecv_coef = ridgecv.coef_
        ridge_df.iloc[i] = ridgecv_coef
        
        #print('Ridge R square', ridgecv_score)        
        #print('Ridge Alpha', ridgecv_alpha )

        # Build "phoney data" (the new dataset can be used in ols, which has the same estimated coefficients in ridge estimation)
        import math
        k = len(factor_ls)
        
        y_ridge = np.append(y_std, np.zeros(k)) #(23,)
        y_df_new.iloc[i] = y_ridge
        
        x_ridge = np.append(x_std, np.identity(k)*math.sqrt(ridgecv_alpha),axis=0) #(23,3)        
        j=0
        for key,value in x_dic_new.items():
            value.iloc[i] = pd.Series(x_ridge[:,j])
            j+=1    
        
    return ridge_df, y_df_new, x_dic_new
