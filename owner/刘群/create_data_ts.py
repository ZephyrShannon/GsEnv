# <codecell>

import numpy as np
import pandas as pd


def create_data_ts(factor_dic ,stock_rtn):
    stock_rtn = stock_rtn.asMatrix()
    dates_ls = np.intersect1d(list(factor_dic.keys()), stock_rtn.index)
    factor_ls = list(factor_dic[dates_ls[0]].columns)
    for date in dates_ls:
        factor_ls = np.intersect1d(factor_ls, factor_dic[date].columns)
    stock_ls = np.intersect1d(factor_dic[dates_ls[0]].index, stock_rtn.columns)
    data_dic = dict()
    for stock in stock_ls:
        temp_dic = dict()
        df = pd.DataFrame(index = dates_ls,columns=factor_ls)
        for date in dates_ls:
            df.loc[date] = factor_dic[date].loc[stock]
        temp_dic['X'] = df.sort_index()
        temp_dic['y'] = stock_rtn.loc[dates_ls,stock]
        data_dic[stock] = temp_dic
    
    # temporarily use one stock for prediction
    return data_dic[stock_ls[0]]


# <codecell>

