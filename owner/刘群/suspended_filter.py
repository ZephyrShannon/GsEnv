# <codecell>

import pandas as pd


def suspended_filter(stocks, suspend_stock):
    
    #suspend_stock_dic = suspend_data_cleaning(suspend_stock)
    
    stock_df = stocks.asMatrix()
    
    stock_suspend_ls = list(set(suspend_stock.keys())&set(stock_df.columns))

    stock_del_ls = []
    
    for stock in stock_suspend_ls:
        if suspend_stock[stock]>= stock_df.index[-1]:
            stock_del_ls.append(stock) 
    
    stock_filter_ls = list(filter(lambda x: x not in stock_del_ls, list(stock_df.columns)))
    stock_df_filtered = stock_df.filter(items=stock_filter_ls)
        
    return stock_df_filtered


# <codecell>

