# <codecell>

import numpy as np
import pandas as pd
from sklearn import linear_model
from lib.gftTools import gftIO
from functools import reduce     
from datetime import datetime           

from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

from lib.gftTools import gsUtils
from datetime import timedelta
import matplotlib.pyplot as plt
from sklearn import datasets, svm
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

def SVM(svmdata,splitpct):
    ls_dates = sorted(list(svmdata.keys()))
    split_cutoff = int(len(ls_dates) * splitpct)
    ls_train_dates = ls_dates[:split_cutoff]
    ls_test_dates=ls_dates[split_cutoff:]
    ###train SVM using train data
    ls_train_data = [svmdata[i] for i in ls_train_dates]
    df_train_data = pd.concat(ls_train_data,axis=0)
    
    df_train_data_clean = df_train_data.dropna(how='any',axis=1)
    df_train_data_clean=df_train_data_clean.drop(['index','y'],axis=1)
    df_x = df_train_data_clean.iloc[:,:-1]
    X=np.array(df_x)
    y=np.array(df_train_data_clean.iloc[:,-1])

    ls_C=[2**(-5),2**(-3),2**(-1),2**(1),2**(3),2**(5),2**(7)]
    ls_gamma=[2**(-15),2**(-13),2**(-11),2**(-9),2**(-7),2**(-5),2**(-3)]

    grid = GridSearchCV(SVC(), param_grid={"C":ls_C, "gamma": ls_gamma}, cv=4)
    grid.fit(X, y)
    model= SVC(kernel='rbf',C=grid.best_params_['C'], gamma=grid.best_params_['gamma'])
    model.fit(X,y)
     
    ####predict test data
    ls_x_name=df_x.columns.values
    dict_test_x={i:svmdata[i].reindex(columns=ls_x_name).fillna(0) for i in ls_test_dates}  
    test_z = {i:pd.DataFrame(data=model.predict(np.array(dict_test_x[i])),index=dict_test_x[i].index,columns=['yhat']) for i in ls_test_dates}
    return test_z

# <codecell>

svmdata=x0
splitpct=x1

# <codecell>


