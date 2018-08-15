# <codecell>

from lib.gftTools import gftIO
from lib.gftTools import gsUtils
import pandas as pd
import numpy as np

def GetRetTrainTest(context,x0,train_period,train_snapshot,refit_period,binnumber,asc):
    ##step1:data prepare

    df_ret=x0.asMatrix().sort_index().T
    ls_datalist=sorted(list(df_ret.columns))
    len_date=len(ls_datalist)
    if len_date < train_period + train_snapshot:
        raise Exception("not enough train data")
    ls_train_start=list(range(train_period+1,len_date,refit_period))
    ls_newcolraw=list(map(lambda x:'x'+str(x),list(range(0,train_period))))
    ls_newcol=ls_newcolraw+['y']
    
    dict_train_data=[gettraindata(df_ret,ls_datalist,i,train_period,train_snapshot,ls_newcol,ls_newcolraw,binnumber,asc) for i in ls_train_start if i+train_snapshot-1 <= len_date]
    df_train_final=pd.concat(dict_train_data,axis=0)
    
    ls_trainno=list(map(lambda x:int(x),list(np.unique(df_train_final['fitno']))))
    ls_test_start={i:list(range(i+train_snapshot,int(np.where(i+train_snapshot+refit_period<=len_date+1,i+train_snapshot+refit_period,len_date+1)))) for i in ls_trainno if i+train_snapshot <= len_date}
    ls_test_data=[gettestdata(ls_test_start,i,df_ret,train_period,ls_datalist,ls_newcolraw,binnumber,asc) for i in list(ls_test_start.keys())]
    df_test_final=pd.concat(ls_test_data,axis=0)
    

    dict_train_test_data={'train':df_train_final,'test':df_test_final}
    return dict_train_test_data

def gettraindata(df_ret,ls_datalist,i,train_period,train_snapshot,ls_newcol,ls_newcolraw,binnumber,asc):
    dict_train={ls_datalist[j-2]:df_ret.iloc[:,j-train_period-1:j].copy() for j in list(range(i,i+train_snapshot))}
    discretize(dict_train,ls_newcol,ls_newcolraw,binnumber,asc)  
    ls_train=[dict_train[i] for i in list(dict_train.keys())]
    df_train=pd.concat(ls_train,axis=0)
    df_train=df_train.assign(fitno=float(i))
    return df_train

def gettestdata(ls_test_start,i,df_ret,train_period,ls_datalist,ls_newcolraw,binnumber,asc):
    dict_test={ls_datalist[j-1]:df_ret.iloc[:,j-train_period:j].copy() for j in ls_test_start[i]}
    discretize(dict_test,ls_newcolraw,ls_newcolraw,binnumber,asc) 
    ls_test=[ dict_test[key] for key in dict_test.keys()]
    df_test_onetrain=pd.concat(ls_test,axis=0)
    df_test_onetrain=df_test_onetrain.assign(fitno=float(i))
    return df_test_onetrain
    
def discretize(data,newcolname,discretname,binnumber,asc):
    if asc==1:
        asc=True
    else:
        asc=False        
    for key in list(data.keys()):
        temp=data[key].copy()
        temp.dropna(how='any',inplace=True)
        temp.columns=newcolname     
        temp.reset_index(inplace=True)
        temp[discretname]=pd.DataFrame(temp[discretname].apply(lambda x:gsUtils.cut2bin(x,binnumber,ascending=asc)),dtype='float')
        temp['snapshot']=key
        data[key]=temp  

# <codecell>



# <codecell>


