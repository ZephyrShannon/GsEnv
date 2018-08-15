# <codecell>




def drop_fillna(factor_dic, na_pct, fill_value):
    date_ls = list(factor_dic.keys())
    non_na = round(factor_dic[date_ls[0]].shape[0]*(1-na_pct))
    for date in date_ls:
        factor_dic[date].dropna(axis=1, thresh = non_na,inplace=True) # drop the factor having na > na_pct
        factor_dic[date].fillna(value=fill_value, inplace=True)
    return factor_dic



# <codecell>

