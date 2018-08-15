# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils
def ExtractDic(dic, retain_or_not, names):
    all_names = names.split(',')
    digit_or_not = []
    all_keys = list(dic.keys())
    if len(all_keys) == 0:
        raise Exception('No keys selected') 
    for i in all_names:
        if i not in all_keys:
            raise Exception('key not exist') 
    new_dic = []
    if retain_or_not:
        for i in all_keys:
            if (type(dic[i]) == int) or (type(dic[i]) == float) or (type(dic[i]) == np.int64)\
            or  (type(dic[i]) == np.float64) or (type(dic[i]) == pd.Timestamp)or (i in all_names):
                new_dic = dict(new_dic, **{i:dic[i]})
    else:
        for i in all_keys:
            if i in all_names:
                new_dic = dict(new_dic, **{i:dic[i]})   
    if len(new_dic.keys()) == 1:
        output = new_dic[list(new_dic.keys())[0]]
    else:
        output = new_dic        
    return output
        
