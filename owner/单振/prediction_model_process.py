# <codecell>

import numpy as np
import pandas as pd
import xarray as xr

# <codecell>

def prediction_model_process(context, dic_Xs, y, align_and_sample_func, split_func, remedy_func, regress_func, socre_func, args):
    axis = args.get('axis', 0)
    if axis == 1:
        windows_size = args.get("windows_size")
        if windows_size is None:
            raise Exception("windows size is not set.")
    else:
        windows_size = 0
        
    # 1st get intersect data
    all_data = dic_Xs.copy()
    all_data['y'] = y
    alinged_data = align_and_sample_func(all_data)
    
    # 2nd split the train data
    splited_datas = dict()
    for key, item in aligned_data:
        splited_datas[key] = split_func(item, axis)
        
    # 3rd repair the datas
    if remedy_func is not None:
        splited_datas = remedy_func(splited_datas, test_on = 'train')
    

    # 4th do regress
    train_datas = dict()
    test_datas = dict()
    for key, item in splited_datas:
        train_datas[key] = item['train']
        test_datas[key] = item['test']

    train_y = train_datas.pop('y')
    test_y = test_datas.pop('y')
    
    train_x_array = xr.Dataset(train_datas).to_array(dim='factor')
    model_data = regress_func(train_x_array, train_y, axis, windows_size)
        
    # 5th get score for the result.
    if score is not None:
        test_x_array = xr.Dataset(test_datas).to_array(dim='factor')
        score = socre_func(model_data, test_x_array, test_y, axis, windows_size)
        return {'model': model_data, 'score': score}
    return {'model':model_data, 'score': None}
        

# <codecell>

