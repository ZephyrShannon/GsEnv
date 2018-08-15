# <codecell>

import pandas as pd
import numpy as np

def stock_selection_decision_tree(factor_dic ,stock_rtn ,max_depth ,min_samples_split ,min_decrease ,criterion):
        
    # create required data format
    data_df, factors_ls = create_data_df(factor_dic, stock_rtn)
    
    # build tree
    tree, ls = build_tree(data_df, factors_ls, max_depth, min_samples_split, min_decrease, criterion)
    
    # put end leaves(dataframes) to dictionary
    dic_keys = list(map(lambda x:'group'+str(x), list(range(0,len(ls)))))
    dic = dict(zip(dic_keys, ls))
    
    return dic

# <codecell>

def create_data_df(factor_dic, stock_rtn):
    
    stock_df = stock_rtn.asMatrix().T #[symbols, date]
    date_ls = list(factor_dic.keys())
    

    factor_ls=[]
    xy_ls = []
    for date in date_ls:        
        # factors may be different in different dates
        factors = list(factor_dic[date].columns)
        factor_ls = list(set(factor_ls)|set(factors))
    
        factor_df = factor_dic[date]
        date_stamp = pd.DatetimeIndex([date])[0]
        xy_df = pd.concat([factor_df, stock_df[date]],axis=1).rename(columns={date_stamp:'y'})
        xy_df['date']=date
        xy_ls.append(xy_df)
    
    # it has been intersected in previous steps, so the symbols should have been aligned
    data_df = pd.concat(xy_ls)

    return data_df, factor_ls
    

# <codecell>

# Build a decision tree
def build_tree(data_df, factors_ls, max_depth, min_samples_split, min_decrease, criterion):
    ls=[]
    # root of the sample data by finding the lowest mse: dict{factor_index, threshold, mse, left_right_df}
    root = get_split(data_df, factors_ls, criterion)
    # get left and right nodes
    split(root, ls, factors_ls, max_depth, min_samples_split, 1, min_decrease, criterion)
    return root, ls

# <codecell>

def get_split(data_df, factors_ls, criterion):

    b_score = float('inf')

    for factor in factors_ls:
        range_max = data_df[factor].max()
        range_min = data_df[factor].min()
        for threshold in np.linspace(range_min,range_max,20): # contruct all possibile pairs to compare
            groups = test_split(factor, threshold, data_df)
            if groups[0].empty or groups[1].empty:
                continue                   
            
            # mse: threshold score is the sum mse of y in left and right group
            impurity = impurity_index(groups, criterion)# find the index with lowest weighted impurity from each branch
            if impurity <= b_score:
                b_index, b_value, b_score, b_groups = factor, threshold, impurity, groups

    return {'factor':b_index, 'threshold':b_value, 'score':b_score,'groups':b_groups}


# <codecell>

def test_split(factor, threshold, data_df):
    left, right = data_df[data_df[factor]<threshold], data_df[data_df[factor]>=threshold]
    return left, right

# <codecell>

def impurity_index(groups, criterion):
    n_l = len(groups[0])
    n_r = len(groups[1])
    n = n_l+n_r

    if criterion == 'kl':
        bin_range = max(n_l,n_r)
        pdf_l = pdf(groups[0]['y'], bin_range)
        pdf_r = pdf(groups[1]['y'], bin_range)
        impurity = kl_index(pdf_l,pdf_r)

    if criterion == 'gini':
        pdf_l = pdf(groups[0]['y'],'auto')
        pdf_r = pdf(groups[1]['y'],'auto')
        impurity_l = gini_index(pdf_l)
        impurity_r = gini_index(pdf_r)
        impurity = n_l / n * impurity_l + n_r / n * impurity_r

    if criterion == 'mse':
        impurity_l = mse_index(groups[0])
        impurity_r = mse_index(groups[1])
        impurity = n_l / n * impurity_l + n_r / n * impurity_r

    if criterion == 'wasserstein':
        impurity = - wasserstein_index(groups)

    return impurity

# <codecell>

def pdf(data,bin_range):
    hist, bin_edges = np.histogram(data,bins=bin_range, density = True)
    pdf_arr = hist * (bin_edges[1:]-bin_edges[:-1])
    return pdf_arr

# averaged variance
def mse_index(data_df):
    mse = np.var(data_df['y'])/len(data_df)
    return mse 

# wasserstein distance between two distributions
def wasserstein_index(groups):
    from scipy.stats import wasserstein_distance
    wd = wasserstein_distance(groups[0]['y'].values, groups[1]['y'].values)
    return wd

def gini_index(p):
    gini_index = 1- np.sum(np.square(p))
    return gini_index
        
def kl_index(p,q):
    # q is a dominator, so we set a small number np.finfo(np.float32).eps = 1.1920929e-07 to place zeros 
    np.place(q,q==0,np.finfo(np.float32).eps)
    import scipy.stats
    kl_index = scipy.stats.entropy(p,q)
    return kl_index


# <codecell>


# Create child splits for a node or make terminal
def split(root, ls, factors_ls, max_depth, min_samples_split, depth, min_decrease, criterion):
    left, right = root['groups'] # df
    del(root['groups'])
    # check for a no split
    if len(left) == 0 or len(right) ==0:
        onegroup = pd.concat([left,right])
        root['left'] = root['right'] = to_terminal(onegroup)
        ls.append(onegroup)
        return
    # check for max depth
    if depth >= max_depth:
        root['left'], root['right'] = to_terminal(left), to_terminal(right)
        ls.append(left)
        ls.append(right)
        return
    # process left child
    if len(left) <= min_samples_split:
        root['left'] = to_terminal(left)
        ls.append(left)
    else:
        temp=get_split(left, factors_ls, criterion)
        if abs(root['score'] - temp['score']) <= min_decrease:###若mse decrease < 0.00001，那么就stop
            root['left'] = to_terminal(left)
            ls.append(left)
        else:
            root['left'] = temp##这里的结果就是dict里面套一个dict
            split(root['left'], ls, factors_ls, max_depth, min_samples_split, depth+1, min_decrease, criterion)

    # process right child
    if len(right) <= min_samples_split:
        root['right'] = to_terminal(right)
        ls.append(right)
    else:
        temp=get_split(right,factors_ls, criterion)
        if abs(root['score'] - temp['score']) <= min_decrease:
            root['right'] = to_terminal(right)
            ls.append(right)
        else:
            root['right'] = temp
            split(root['right'], ls, factors_ls, max_depth, min_samples_split, depth+1,min_decrease, criterion)

# Create a terminal node value
def to_terminal(group):
    return group


# <codecell>

