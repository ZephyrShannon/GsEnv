# <codecell>

# Your code goes here.
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# bunches of scoresssss
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

_CLASSIFIER = RandomForestClassifier()

def RandomForest(df_x,df_y,winSize,winStep):
    '''
    -------- parameter----------
    DataFrame:{columns=["date","x1","x2", ..., "xn"]}
    DataFrame:{columns=["date","y"]}
    winSize: float
    winSteop: float
    
    ---------return----------
    DataFrame:{columns=["date","y"]}
    
    assumption:
    1. 'xi' has been sorted by 'date'
    2. 'y' cloumn in 'X0' has been shifted
        
    '''

    if isinstance(df_x, gftIO.GftTable):
        df_x = df_x.asColumnTab()
    if isinstance(df_y,dict):
        df_y = df_y["y"]
    if isinstance(df_y, gftIO.GftTable):
        df_y = df_y.asColumnTab()
    
    # convert parameter type
    winSize = int(winSize)
    winStep = int(winStep) 
    
    # NOTICE: integer will be regraged as O by GS, but classifier need int
    value_column = _findValueColumn(df_y.columns)  # value_column: value  
                                                   # df_y.columns:Index(['date', 'value'], dtype='object')
    df_y.rename(columns={value_column:"y"},inplace=True)
    df_y.y=pd.factorize(df_y.y)[0]
    # change column name
    for col_name in df_y.columns:
        if isinstance(df_y.ix[0,col_name],pd.Timestamp):
            df_y.rename(columns={col_name:"date"},inplace=True)
            break
    # remove meanless columns
    df_y=df_y[["date","y"]]
    
    # merge data
    df_x = df_x.sort_values("date",ascending=True)
    df_y = df_y.sort_values("date",ascending=True)
    df_y = df_y.set_index(np.arange(len(df_y))) # indentify index: start from 0

    # frequency error: if y_freq > x_freq, meanless data
    ls_missing_date=[d for d in list(df_y["date"]) if d not in list(df_x["date"])]
    if len(ls_missing_date)>0:
        raise ValueError("y_freq > x_freq. Missing date in X:", ls_missing_date)
    
    # slice data: remove redundant x
    if len(df_x)!=len(df_y):
        ls_slice_data=[d for d in list(df_x["date"]) if d not in list(df_y["date"])]
        df_tmp_x=df_x.set_index(["date"])
        df_tmp_x=df_tmp_x.drop(ls_slice_data)
        df_x=df_tmp_x.reset_index(np.arange(len(df_tmp_x)),drop=False)
    
    # identify index: start from 0
    df_x = df_x.set_index(np.arange(len(df_x)))
    df_y = df_y.set_index(np.arange(len(df_y))) 

    # data to be trained
    df_data=pd.merge_ordered(df_x,df_y,on="date",how="outer") 

    # value check
    if len(df_data.index) < winSize + 1:
        raise ValueError("the number of input data is not enough")
    
    # rooling
    ls_predicted=[]
    for i in range(len(df_data.index)):
        if i<winSize:
            ls_predicted+=[np.nan]
        else:
            start_index=i-winSize
            # fit
            n_x_train= df_data.iloc[start_index:i,1:-1].values
            n_y_train= df_data.iloc[start_index:i,-1].values
            _CLASSIFIER.fit(n_x_train, n_y_train)
            # predict
            n_x_test = df_data.iloc[[i],1:-1]
            y_test = _CLASSIFIER.predict(n_x_test)[0]
            ls_predicted += [y_test]
    
    df_data["predicted"]=ls_predicted
    #print(ls_predicted)
    
    # drop na
    df_data=df_data.dropna()
    #print(df_data)
    
    # scoressssssss
    y_true=pd.factorize(df_data["y"])[0]
    y_pred=pd.factorize(df_data["predicted"])[0]
    num_accuracy_score=accuracy_score(y_true,y_pred)
    #print("accuracy_score:",num_accuracy_score)
    num_f1_score=f1_score(y_true,y_pred,average='macro') # micor, weighted, None
    #print("f1_score:",num_f1_score)
    num_precision_score=precision_score(y_true, y_pred, average='macro') # micor, weighted, None
    #print("precision_score:",num_precision_score)
    num_recall_score=recall_score(y_true, y_pred, average='macro') # micor, weighted, None
    #print("recall_score:",num_recall_score)
    dict_score={"accuracy_score":num_accuracy_score, "f1_score":num_f1_score,"precision_score":num_precision_score, "recall_score":num_recall_score}
    
    # score
    y_test = df_data["predicted"].values
    X_test = df_data.iloc[:,1:-2].values
    num_mean_accuracy=_CLASSIFIER.score(X_test , y_test)
    #print(num_score)    
    
    '''
    # feature_importances
    ls_fitness=list(zip(df_data.iloc[:,1:-1],_CLASSIFIER.feature_importances_))
    n_fitness=np.array(list(map(list,ls_fitness)))
    df_fitness=pd.DataFrame({"feature":n_fitness[:,0],"importance":n_fitness[:,1]})
    #print(df_fitness)    
    '''
    
    # result
    df_data=df_data[["date","predicted"]]
    #print(df_data)
    
    dict_result = {"result":df_data,"mean_accuracy":num_mean_accuracy, "scores":dict_score} #,"fitness":df_fitness}
    #print(dict_result)
    return dict_result

def _findValueColumn(ls_columns):
    for acolumn in ls_columns:
        if acolumn.upper() in ["VALUE","VAL","V"]:
            return acolumn
    raise ValueError("Value Column isnot found in {}!".format(ls_columns))
