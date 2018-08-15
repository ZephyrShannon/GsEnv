# <codecell>

import pandas as pd

def drop_na(data):

    factor_ls = list(data.keys())
    date_ls = list(data[factor_ls[0]].index)
    symbol_ls = list(data[factor_ls[0]].columns)
    new_dict = {}
    

    for date in date_ls:
        df = pd.DataFrame()
        for factor in factor_ls:    
            factor_symbol_df = pd.DataFrame(data[factor].loc[date].values, index = symbol_ls, columns=[factor])
            df = df.append(factor_symbol_df)
        df = df.dropna(axis=0, how='all').fillna(0)
        if df.empty:
            continue
        else:
            new_dict[date] = df
    
    return new_dict
    


# <codecell>

