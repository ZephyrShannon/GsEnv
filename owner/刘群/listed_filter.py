# <codecell>

import pandas as pd
import datetime


def listed_filter(stocks, listed_dates, remove_days):
      
    stock_df = list(stocks.values())[0]
    stock_list_date = list(listed_dates.values())[0]
    
    del_datepoint = stock_df.index[-1] - datetime.timedelta(days = remove_days)

    stock_del_df = stock_list_date[stock_list_date['idname']>del_datepoint]
    stock_del_ls = stock_del_df['variable'].tolist()
    stock_filter_ls = list(filter(lambda x: x not in stock_del_ls, list(stock_df.columns)))
    stock_df_filtered = stock_df.filter(items=stock_filter_ls)
    
    stock_filtered_dic = {'listed_filter': stock_df_filtered}
    
    return stock_filtered_dic


# <codecell>

