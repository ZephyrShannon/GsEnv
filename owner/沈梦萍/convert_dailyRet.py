# <codecell>

import numpy as np
import pandas as pd

def convert_dailyRet(price,freq):
    if freq in (0,10,11,50):
        raise ValueError('Does not support!Please choose other options')
    price = price.dropna(axis=1,how='all') #remove non-business days
    monthly_price = price.resample('M').last()
    quarterly_price = price.resample('Q').last()
    weekly_price = price.resample('W-FRI').first()
    yearly_price = price.resample('A').last()
    
    if freq == 20: #weekly
        result = weekly_price
    elif freq == 30:
        result =  monthly_price
    elif freq == 40:
        result= quarterly_price
    elif freq == 60:
        result =  yearly_price
    
    tot_return_index = result.pct_change(1)
    df_l_tot_return_index =  gftIO.convertMatrix2ColumnTab(tot_return_index)
    df_l_tot_return_index = df_l_tot_return_index.dropna()
    df_l_tot_return_index.columns= ['date','symbol','ret']
    result = df_l_tot_return_index.sort_values('date')
    final_result = {'result':result}
    return final_result 


    
    
