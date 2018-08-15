# <codecell>

import numpy as np
import pandas as pd



def intersect_with_trading_universe(stock, factor):
    stock_rtn_df = stock.asMatrix() # monthly(320, 2832)
    factor_dic = factor

    factor_ls = list(factor_dic.keys())
    stock_ls = list(stock_rtn_df.columns)

    stock_dates = list(stock_rtn_df.index)

    x_dic=dict()

    for factor in factor_ls:
        stock_df = factor_dic[factor]

        # delete stocks that is not in the trading universe
        stock_in_factor = list(filter(lambda x: x in stock_ls, list(stock_df.columns)))
        df = stock_df.reindex(columns=stock_in_factor)

        # align dates based on stock_dates
        df_final = df.reindex(stock_dates, method = 'nearest')

        x_dic[factor] = df_final
    

    return x_dic


# <codecell>

