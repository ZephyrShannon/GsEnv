# <codecell>

import numpy as np
import pandas as pd
import random
# {}


def train_test_split(data, split_method, axis, args):
    '''
       Input:
           split_method: 0 for split in order; 1 for split randomly
           dict_arg: {'pct4train': percentage of training dataset,
                      'pct4test': percentage of testing dataset, 
                      'pct4valid': percentage of validation dataset,
                      'seeds': a seed when we use random split method}

               when seeds==0, we use pure random
       Output:
           output={'train':dict_train, 'test':dict_test,'valid':dict_valid}
       '''
    if isinstance(axis, str):
        axis = int(axis)

    pct4train = args['pct4train']/100  # pct4train is mandatory
    pct4test = args['pct4test']/100  # pct4test is mandatory
    pct4valid = args.get('pct4validation')/100
    if pct4valid is None:
        left = 1 - (pct4train + pct4test)
        if left < pct4valid:
            pct4valid = left

    seeds = args.get('seeds')

    if seeds is not None:
        random.seed(seeds)

    if isinstance(data, gftIO.GftTable):
        df_4_slice = data.as_matrix()
    elif isinstance(data, pd.DataFrame):
        df_4_slice = data
    else:
        raise Exception("Not acceptable data of type:{0}".format(str(type(data))))

    ls_date = df_4_slice.index
    ls_symbol = df_4_slice.columns

    if axis == 0:  # which means index
        data_size = ls_date.size
        rand_data = ls_date
    else:
        data_size = ls_symbol.size
        rand_data = ls_symbol

    if pct4valid > 0:
        train_num = int(np.floor(data_size * pct4train))
        test_num = int(np.floor(data_size * pct4train))
        validation_num = data_size - train_num - test_num
    else:
        train_num = int(np.floor(data_size * pct4train))
        test_num = data_size - train_num
        validation_num = 0

    train_set = set(random.sample(rand_data.tolist(), train_num))
    remains_in_pool = set(rand_data) - train_set
    if validation_num <= 0:
        test_set = remains_in_pool
        validation_set = None
    else:
        test_set = set(random.sample(remains_in_pool, test_num))
        validation_set = remains_in_pool - test_set

    ret = dict()
    if axis == 0:
        ret['train'] = df_4_slice.loc[train_set, ls_symbol]
        ret['test'] = df_4_slice.loc[test_set, ls_symbol]
        if validation_num > 0:
            ret['validation'] = df_4_slice.loc[validation_set, ls_symbol]
    else:
        ret['train'] = df_4_slice.loc[ls_date, train_set]
        ret['test'] = df_4_slice.loc[ls_date, test_set]
        if validation_num > 0:
            ret['validation'] = df_4_slice.loc[ls_date, validation_set]

    return ret


# ##BEGIN AUTO CREATE CODE##

def get_desc_generator():
    return gsMeta.DescGenerator.create_default()
# end

# ##END AUTO CREATE CODE ##

# ##BEGIN CODES FOR CREATE_LAMBDA##

def get_func():
    return train_test_split

def create_func_obj(data, split_method, axis, args):
    return gftIO.GsFuncObj('9A26AFA646404690A92853304FF2D1E0', '81CEDCD5291A4E8FAE4042061B71670D', train_test_split,  False, data, split_method, axis, args)
# end 

# ##END CODES FOR CREATE_LAMBDA##

