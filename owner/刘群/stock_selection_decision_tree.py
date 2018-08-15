# <codecell>

import pandas as pd
import numpy as np


def stock_selection_decision_tree(stock_rtn ,factor_dic ,max_depth ,min_samples_split ,min_decrease ,criterion, date):
    # closest date
    date_ls = list(factor_dic.keys())
    closest_date = min(date_ls, key = lambda x: abs(x - date))
    
    data_df = combine_data(stock_rtn, factor_dic, closest_date)


# <codecell>

 def combine_data (stock_rtn, factor_dic, date):
        factor_ls = list(factor_dic.keys())
        data_df = factor_dic[date]
        data_df['y'] = stock_rtn
        return data_df
        

# <codecell>



# <codecell>



# <codecell>



# <codecell>



# <codecell>

