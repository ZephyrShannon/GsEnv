# <codecell>

from lib.gftTools import gftIO
from lib.gftTools import gsUtils
import pandas as pd
import numpy as np
import random

def PastReturnPredict(context,x0,train_period,train_snapshot,test_period,max_depth,min_size,sample_size,n_features,n_trees,min_decrease):
    ##step1:data prepare    
    #df_dataset=x0.asMatrix().sort_index().fillna(method='ffill').T
    df_dataset=x0.asMatrix().sort_index().T
    ls_datalist=sorted(list(df_dataset.columns))
    len_date=len(ls_datalist)
    if len_date < train_period + train_snapshot:
        raise Exception("not enough train data")
    ls_train_start=list(range(train_period+1,len_date,test_period))
    dict_train_data={i:gettraindata(df_dataset,ls_datalist,i,train_period,train_snapshot) for i in ls_train_start if i+train_snapshot-1 <= len_date}
    
    ls_test_start={i:list(range(i+train_snapshot,int(np.where(i+train_snapshot+test_period<=len_date+1,i+train_snapshot+test_period,len_date+1)))) for i in dict_train_data.keys() if i+train_snapshot <= len_date}
    
    dict_test_data={i:gettestdata(ls_test_start,i,df_dataset,train_period,ls_datalist) for i in list(ls_test_start.keys())}
    ##step2:strategy creation   
    
    ls_test_key=list(dict_test_data.keys())[-4:]
    
    dict_train_tree={i:random_forest(dict_train_data, dict_test_data, i,max_depth, min_size, sample_size, n_trees, n_features,min_decrease)  for i in ls_test_key}
    ls_train_tree=[dict_train_tree[i] for i in dict_train_tree.keys()]
    return pd.concat(ls_train_tree,axis=0)
   

def gettraindata(df_dataset,ls_datalist,i,train_period,train_snapshot):
    dict_train={ls_datalist[j-2]:df_dataset.iloc[:,j-train_period-1:j].copy() for j in list(range(i,i+train_snapshot))}
    
    ls_newcolraw=list(map(lambda x:'x'+str(x),list(range(0,train_period))))
    ls_newcol=ls_newcolraw+['y']
    for key in list(dict_train.keys()):
        temp=dict_train[key].copy()
        temp.dropna(how='any',inplace=True)
        temp.columns=ls_newcol      
        temp.reset_index(inplace=True)
        temp[ls_newcolraw]=temp[ls_newcolraw].apply(lambda x:gsUtils.cut2bin(x,10, ascending=True))
        temp['snapshot']=key
        dict_train[key]=temp
        
    ls_train=[dict_train[i] for i in list(dict_train.keys())]
    df_train=pd.concat(ls_train,axis=0)
    return df_train
    
    
def gettestdata(ls_test_start,i,df_dataset,train_period,ls_datalist):
    dict_test={ls_datalist[j-1]:df_dataset.iloc[:,j-train_period:j].copy() for j in ls_test_start[i]}
    
    ls_newcol=list(map(lambda x:'x'+str(x),list(range(0,train_period))))
    for key in list(dict_test.keys()):
        
        temp=dict_test[key].copy()
        temp.dropna(how='any',inplace=True)
        temp.columns=ls_newcol      
        temp.reset_index(inplace=True)
        temp[ls_newcol]=temp[ls_newcol].apply(lambda x:gsUtils.cut2bin(x,10, ascending=True))
        temp['snapshot']=key
        dict_test[key]=temp
    return dict_test
    

# Random Forest Algorithm
def random_forest(dict_train_data, dict_test_data, i,max_depth, min_size, sample_size, n_trees, n_features,min_decrease):
    df_train=dict_train_data[i].drop(['snapshot','symbol'],axis=1)
    #train=[df_train.iloc[i,:] for i in range(len(df_train))]
    trees = list()
    ls_x=list(df_train.columns)[:-1]
    max_depth = ((2 ** 31) - 1 if max_depth is None
                    else max_depth)
    ##train data
    for n_tree in range(n_trees):
        sample=df_train.sample(n=round(len(df_train) * sample_size),replace=True)
        
        #sample = subsample(train, sample_size)##有放回的随机抽样
        tree = build_tree(sample,ls_x, max_depth, min_size, n_features,min_decrease)##造树
        trees.append(tree)
        
    ##predict data    
    predictions = [bagging_predict(trees,dict_test_data,i,date) for date in list(dict_test_data[i].keys())]##对test数据集中每个观测进行predict
    df_pre=pd.concat(predictions,axis=0) 
    df_pre_max=df_pre.pivot_table(values='wgt', index='date', columns='symbol')
    return df_pre_max

# Build a decision tree
def build_tree(train,ls_x, max_depth, min_size, n_features,min_decrease):
    root = get_split(train, ls_x,n_features)
    split(root, ls_x,max_depth, min_size, n_features, 1,min_decrease)
    return root

# Select the best split point for a dataset
def get_split(train, ls_x,n_features):##每次split，都要重新不放回抽样一遍feature
    #class_values = list(set(row[-1] for row in train))
    b_score=999999
    features=random.sample(ls_x,n_features)

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
def split(node, ls_x,max_depth, min_size, n_features, depth,min_decrease):    
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
    if len(left) <= min_size:
        node['left'] = to_terminal(left)
    else:
        temp=get_split(left, ls_x,n_features)
        if node['score'] - temp['score'] <= min_decrease:###若mse decrease < 0.00001，那么就stop
            node['left'] = to_terminal(left)
        else:
            node['left'] = temp##这里的结果就是dict里面套一个dict
            split(node['left'], ls_x,max_depth, min_size, n_features, depth+1,min_decrease)
            
	# process right child
    if len(right) <= min_size:
        node['right'] = to_terminal(right)
    else:
        temp=get_split(right,ls_x, n_features)
        if node['score'] - temp['score'] <= min_decrease:
            node['right'] = to_terminal(right)
        else:
            node['right'] = temp
            split(node['right'],ls_x, max_depth, min_size, n_features, depth+1,min_decrease)

# Create a terminal node value
def to_terminal(group):##如果是叶节点，那么返回该叶节点下期stock return的均值作为预测值
    return np.mean(group['y'])
  
# Make a prediction with a list of bagged trees
#def bagging_predict(trees,dict_test_data[i],date):
def bagging_predict(trees,dict_test_data,i,date):
    temp=dict_test_data[i][date]
    df_one_test=dict_test_data[i][date].drop(['snapshot','symbol'],axis=1)
    ser_onetest=df_one_test.apply(lambda x:tree_pre(x,trees),axis=1)
    ser_rank=pd.DataFrame(data=gsUtils.cut2bin(ser_onetest,10, ascending=True),columns=['rank'])
    df_rank=pd.concat([ser_rank,temp],axis=1)
    wgt=1/len(df_rank[df_rank['rank']==10])
    df_fnl=df_rank[df_rank['rank']==10][['symbol']].assign(wgt=wgt)
    return df_fnl.assign(date=date)
    
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


