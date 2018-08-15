# <codecell>




def create_y_dictionary(stock_close_price, benchmark, index_weight, stock_list_date, stock_suspend_date):
    dict={}
    dict['stock_close_price']= stock_close_price.asMatrix()
    dict['benchmark'] =benchmark.asMatrix()
    dict['index_weight'] =index_weight.asColumnTab() # including industrial code
    dict['stock_list_date']=stock_list_date.asColumnTab().dropna()
    dict['stock_suspend_date']=suspend_data_dic(stock_suspend_date) # stock as dic keys, dates are in series
    return dict


# <codecell>

def suspend_data_dic(stock_suspend_date):
    x4_df = stock_suspend_date.asColumnTab().dropna().groupby('value').get_group(1)
    x4_group = x4_df.groupby('variable',squeeze=True)
    dic ={}
    for name,group in x4_group:
        dic[name]=group['idname']
    return dic

# <codecell>

