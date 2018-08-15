# <codecell>

from lib.gftTools import gftIO
from lib.gftTools import gsUtils
import pandas as pd
import numpy as np
import random

def ZimmermanModel(context,trainData,testData,Params):
    ##step1:get train test data
    df_train_data=trainData.asColumnTab()
    df_test_data=testData.asColumnTab()
    
    ##step2:get random forest params
    ls_union_columns = list(set(df_train_data.columns).intersection(set(df_test_data.columns)))
    df_train_data=df_train_data.reindex(columns=ls_union_columns)
    df_test_data=df_test_data.reindex(columns=ls_union_columns)
    
    min_decrease=Params['min_decrease']
    max_features=Params['max_features']
    sample_size=Params['sample_size']
    min_samples_split=Params['min_samples_split']
    max_depth=Params['max_depth']
    n_estimators=Params['n_estimators']  
    max_depth = ((2 ** 31) - 1 if max_depth == 999
                    else max_depth)
    
    ls_date_test=list(np.unique(list(df_test_data.date)))
    dict_train_tree=random_forest(df_train_data,df_test_data,min_decrease,max_features,sample_size,min_samples_split,max_depth,n_estimators,ls_date_test)
    
    dict_train_tree_final =dict(Params,**dict_train_tree)
    return dict_train_tree_final
    

# Random Forest Algorithm
def random_forest(df_train_data,df_test_data,min_decrease,max_features,sample_size,min_samples_split,max_depth,n_estimators,ls_date_test):
    df_train=df_train_data.drop(['symbol','date'],axis=1)
    trees = list()
    ls_x= [i for i in list(df_train.columns) if i != 'y']

    ##train data
    for n_tree in range(n_estimators):
        sample=df_train.sample(n=round(len(df_train) * sample_size),replace=True)
        tree = build_tree(sample,ls_x, max_depth, min_samples_split, max_features,min_decrease)##造树
        trees.append(tree)
        
    ##predict test data    
    predictions = [bagging_predict(trees,df_test_data,date) for date in ls_date_test]##对test数据集中每个观测进行predict
    df_pre=pd.concat(predictions,axis=0) 
    
    ##predict train data
    ls_train_date =list(np.unique(list(df_train_data.date)))
    predictions_train = [bagging_predict(trees,df_train_data,date) for date in ls_train_date]##对test数据集中每个观测进行predict
    df_pre_train=pd.concat(predictions_train,axis=0) 
    
    ##calculate constant_global_mean
    constant_global_mean=np.mean(df_train_data.y)
    
    ##calculate train mse
    df_train_residual=calResidual(df_pre_train,constant_global_mean)
    ##calculate test mse
    ls_test_residual=[calResidual(df_pre[df_pre['date'] == date],constant_global_mean).assign(date=date) for date in ls_date_test]
    df_test_residual = pd.concat(ls_test_residual,axis=0)
    
    return {'prediction_test':df_pre,'train_Residual':df_train_residual,'test_Residual':df_test_residual}

def calResidual_final(data,trees,constant_global_mean):
    temp=data.copy()
    df_one_test=temp.drop(['date','symbol','y'],axis=1)
    ls_residual_raw=[tree_predict_residual(df_one_test,tree,temp,i,constant_global_mean) for tree,i in zip(trees,range(len(trees)))]
    df_residual_raw = pd.concat(ls_residual_raw,axis=0)
    df_residual_raw_final=pd.DataFrame(data=[[np.mean(df_residual_raw['diff'])]],columns=['diff_avg_tree'])
    return df_residual_raw_final
    
def tree_predict_residual(df_one_test,tree,temp,i,constant_global_mean):
    rawdata=temp.copy()
    x=df_one_test.copy()
    rawdata['yhat']= x.apply(lambda x:predict(tree, x),axis=1)
    rawdata_copy=rawdata.copy()
    return calResidual(rawdata_copy,i,constant_global_mean)
    

def calResidual(data,constant_global_mean):
    var_after=sum((data.y-data.yhat)**2)/data.shape[0]
    std_after=np.sqrt(var_after)
    var_before=sum((data.y-constant_global_mean)**2)/data.shape[0]
    std_before=np.sqrt(var_before)
    df_residual=pd.DataFrame(data=[[std_after,std_before]],columns=['std_after','std_before'])
    df_residual['diff']=df_residual['std_before']-df_residual['std_after']
    return df_residual 
    


# Build a decision tree
def build_tree(train,ls_x, max_depth, min_samples_split, max_features,min_decrease):
    root = get_split(train, ls_x,max_features)
    split(root, ls_x,max_depth, min_samples_split, max_features, 1,min_decrease)
    return root

# Select the best split point for a dataset
def get_split(train, ls_x,max_features):##每次split，都要重新不放回抽样一遍feature
    #class_values = list(set(row[-1] for row in train))
    b_score=999999
    features=random.sample(ls_x,max_features)

    for index in features:
        for i in list(range(1,11)):
            groups = test_split(index, i, train)
            mse = mse_index(groups)
            if mse < b_score:
                b_index, b_value, b_score, b_groups = index, i, mse, groups    
    return {'index':b_index, 'value':b_value, 'score':b_score,'groups':b_groups}

##返回值：用哪个变量分割，threshold是什么，返回split之后的两个节点
# Split a dataset based on an attribute and an attribute value
def test_split(index, value, train):
    left, right = train[train[index] <value],train[train[index] >=value]
    return left, right
 
# Calculate the mean squared error for a split dataset
def mse_index(groups):
    ls_mse=[np.var(groups[i]['y'])*len(groups[i]) for i in range(len(groups)) if len(groups[i]) != 0]
    mse=sum(ls_mse)
    return mse

# Create child splits for a node or make terminal
def split(node, ls_x,max_depth, min_samples_split, max_features, depth,min_decrease):    
    left, right = node['groups']
    del(node['groups'])
	# check for a no split
    if len(left) == 0 or len(right) ==0:
        onegroup=pd.concat([left,right])
        node['left'] = node['right'] = to_terminal(onegroup)
        return
	# check for max depth

    if depth >= max_depth:
        node['left'], node['right'] = to_terminal(left), to_terminal(right)
        return
	# process left child
    if len(left) <= min_samples_split:
        node['left'] = to_terminal(left)
    else:
        temp=get_split(left, ls_x,max_features)
        if node['score'] - temp['score'] <= min_decrease:###若mse decrease < 0.00001，那么就stop
            node['left'] = to_terminal(left)
        else:
            node['left'] = temp##这里的结果就是dict里面套一个dict
            split(node['left'], ls_x,max_depth, min_samples_split, max_features, depth+1,min_decrease)
            
	# process right child
    if len(right) <= min_samples_split:
        node['right'] = to_terminal(right)
    else:
        temp=get_split(right,ls_x, max_features)
        if node['score'] - temp['score'] <= min_decrease:
            node['right'] = to_terminal(right)
        else:
            node['right'] = temp
            split(node['right'],ls_x, max_depth, min_samples_split, max_features, depth+1,min_decrease)

# Create a terminal node value
def to_terminal(group):##如果是叶节点，那么返回该叶节点下期stock return的均值作为预测值
    return np.mean(group['y'])
  
# Make a prediction with a list of bagged trees

def bagging_predict(trees,data,date):
    temp=data[data.date==date]
    df_one_test=temp.drop(['date','symbol','y'],axis=1)
    ser_onetest=pd.DataFrame(data=df_one_test.apply(lambda x:tree_pre(x,trees),axis=1),columns=['yhat'])
    df_rank=pd.concat([ser_onetest,temp[['symbol','y','date']]],axis=1)
    return df_rank


def tree_pre(x,trees):
    predictions = [predict(tree, x) for tree in trees]
    return np.mean(predictions)


# Make a prediction with a decision tree
def predict(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']

# <codecell>


