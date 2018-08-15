# <codecell>

import numpy as np
import pandas as pd

# <codecell>


def align_and_resample(dic_datas, freq, lookback, args):
    # args is preserved for future usage.
    o_list = list()
    t_list = list()

    dic_copy = dic_datas.copy()

    for key, data in dic_copy:
        if isinstance(data, gftIO.GftTable):
            data = data.as_matrix()
            dic_copy[key] = data
            o_list.append(data.columns)
            t_list.append(data.index)
        elif isinstance(data, pd.DataFrame):
            o_list.append(data.columns)
            t_list.append(data.index)

    o_set = reduce(lambda x, y: x.intersection(y), o_list)
    t_set = reduce(lambda x, y: x.intersection(y), t_list)
    for key, data in dic_copy:
        dic_copy[key] = data[t_set, o_set]

    # no resample.
    for key, data in dic_copy:
        dic_copy[key] = resample_and_fill_na_matrix(data, freq, lookback)

    return dic_copy

def resample_and_fill_na_matrix(mat: pd.DataFrame, freq, lookback):
    if lookback > mat.index.size:
        lookback = None

    if lookback == None:
        # fill the source first.
        mat = mat.fillna(axis=0, method='ffill')
        # than reindex it.
        return mat.reindex(freq,method='ffill')

    if freq is not None:
        if lookback <= 1:
            return mat.reindex(freq, method='ffill',limit=1)
        else:
            # fillna the remaining lookback - 1 period
            # see data in test2

            mat = mat.fillna(method='ffill',limit=lookback, inplace=False)
            mat_reindex = mat.reindex(freq, method='ffill',limit=1)
            return mat_reindex
    else:
        return mat.fillna(axis=0, method='ffill',limit=lookback)


    

# <codecell>

