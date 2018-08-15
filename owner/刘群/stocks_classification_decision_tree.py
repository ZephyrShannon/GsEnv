# <codecell>

import pandas as pd
import numpy as np


# <codecell>


# count time
import time
start_time=time.time()

def stocks_classification_decision_tree(data, criterion, n_factors):

    #def stock_classification(data, criterion, n_factors):
    max_depth = n_factors
    data_df = data.asColumnTab() # df with symbols
       
    factors_ls = [i for i in list(data_df.columns) if (i!='y' and i!='symbol') ] 

    # parameters of a deep tree
    min_samples_split = 50 # split only when stocks >=100
    min_decrease = 0.00001 # split stop when criterion difference is smaller than 0.00005

    # return a dictionary of ['factor', 'threshold', 'score', 'left', 'right']
    tree = build_tree(data_df, factors_ls, max_depth, min_samples_split, min_decrease, criterion)

    return tree
      
elapsed_time = time.time()-start_time
print('sorting tree takes',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))    


# <codecell>

# Build a decision tree
def build_tree(data_df, factors_ls, max_depth, min_samples_split, min_decrease, criterion):
    # root of the sample data by finding the lowest mse: dict{factor_index, threshold, mse, left_right_df}
    root = get_split(data_df, factors_ls, criterion)
    # create child splits again by selecting from mse
    # get left and right nodes
    split(root, factors_ls, max_depth, min_samples_split, 1, min_decrease, criterion) 
    return root

# <codecell>

# Select the best split point (root node) for a dataset by finding the lowest mse through each factor
def get_split(data_df, factors_ls, criterion):
    if criterion =='mse':
        b_score = float('inf')
    elif criterion=='wasserstein':
        b_score = 0

    for factor in factors_ls:
        range_max = data_df[factor].max()
        range_min = data_df[factor].min()
        for threshold in np.linspace(range_min,range_max,20): # contruct all possibile pairs to compare
            groups = test_split(factor, threshold, data_df)
            if groups[0].empty or groups[1].empty:
                continue                   
            
            # mse: threshold score is the sum mse of y in left and right group
            if criterion == 'mse':               
                mse = mse_index(groups)
                if mse <= b_score: # find the index with lowest mse
                    b_index, b_value, b_score, b_groups = factor, threshold, mse, groups
                    
            elif criterion == 'wasserstein':
                wd = wasserstein_index(groups)
                if wd >=b_score:
                    b_index, b_value, b_score, b_groups = factor, threshold, wd, groups
            

                     
    return {'factor':b_index, 'threshold':b_value, 'score':b_score,'groups':b_groups}


# <codecell>

def test_split(factor, threshold, data_df):
    left, right = data_df[data_df[factor]<threshold], data_df[data_df[factor]>=threshold]
    return left, right

# <codecell>

def mse_index(groups):
    ls_mse=[np.var(groups[i]['y'])/len(groups[i]) for i in range(len(groups)) if len(groups[i]) != 0] #??? mse = var*n was used
    mse=sum(ls_mse)
    return mse 

# <codecell>

def wasserstein_index(groups):
    from scipy.stats import wasserstein_distance
    wd = wasserstein_distance(groups[0]['y'].values, groups[1]['y'].values)
    return wd

# <codecell>

# Create child splits for a node or make terminal
def split(root, factors_ls, max_depth, min_samples_split, depth, min_decrease, criterion):
    left, right = root['groups'] # df
    del(root['groups'])
	# check for a no split
    if len(left) == 0 or len(right) ==0:
        onegroup=pd.concat([left,right])
        root['left'] = root['right'] = to_terminal(onegroup)
        return
	# check for max depth

    if depth >= max_depth:
        root['left'], root['right'] = to_terminal(left), to_terminal(right)
        return
	# process left child
    if len(left) <= min_samples_split:
        root['left'] = to_terminal(left)
    else:
        temp=get_split(left, factors_ls, criterion)
        if root['score'] - temp['score'] <= min_decrease:###若mse decrease < 0.00001，那么就stop
            root['left'] = to_terminal(left)
        else:
            root['left'] = temp##这里的结果就是dict里面套一个dict
            split(root['left'], factors_ls, max_depth, min_samples_split, depth+1,min_decrease, criterion)
            
	# process right child
    if len(right) <= min_samples_split:
        root['right'] = to_terminal(right)
    else:
        temp=get_split(right,factors_ls, criterion)
        if root['score'] - temp['score'] <= min_decrease:
            root['right'] = to_terminal(right)
        else:
            root['right'] = temp
            split(root['right'], factors_ls, max_depth, min_samples_split, depth+1, min_decrease, criterion)
	 

# Create a terminal node value
def to_terminal(group):
    return list(group['symbol'])

# <codecell>

