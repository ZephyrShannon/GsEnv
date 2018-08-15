# <codecell>

import numpy as np
import pandas as pd
from numpy import NaN

def FillWgt(context,close_price,weight,start_date,end_date):
    if start_date >= end_date:
        raise ValueError('startdate should be earlier than enddate!')
    
    if start_date >= end_date:
            raise ValueError('startdate should be earlier than enddate!')
    #Data Prepatation
    df_l_portfolio_wt = weight.asColumnTab().copy()
    df_close_price = close_price.asMatrix()
    
    column_type= gftIO.get_columns_type_dict(df_l_portfolio_wt)
    columns = []
    for key in column_type:
        if column_type[key]==2:
            df_l_portfolio_wt.rename(columns={key:'date'}, inplace=True)
        elif column_type[key]==23:
            df_l_portfolio_wt.rename(columns={key:'weight'}, inplace=True)
        elif column_type[key]==4: 
            columns.append(key)
    df_l_portfolio_wt.rename(columns={columns[0]:'symbol'}, inplace=True)
    df_l_portfolio_wt.rename(columns={columns[1]:'ind'}, inplace=True)
    
    df_l_portfolio_wt = df_l_portfolio_wt.dropna(subset=['weight'])
    df_l_portfolio_wt.sort_values('date',inplace=True)
    df_close_price = df_close_price.dropna(axis = 1, how = 'all')
    #slice dates
    businessdays = df_close_price.index
    if (min(businessdays) > end_date) | (max(businessdays) <start_date):
        raise ValueError ('dates should be reset')
    end_date = max(businessdays[businessdays<=end_date])
    
    alldates = pd.to_datetime(df_l_portfolio_wt['date'].unique())  
    priceDates = alldates
    
    if not(end_date in priceDates):
        priceDates = priceDates.append(pd.Index([end_date])) #add end_date if not included
    
    allSymbols = df_l_portfolio_wt['symbol'].unique()
    df_close_price = df_close_price.reindex(priceDates, allSymbols, fill_value=NaN)   
    
    df_tot_return_index = df_close_price.pct_change(1).shift(-1).fillna(0.0)
    df_l_tot_return_index = gftIO.convertMatrix2ColumnTab(df_tot_return_index)
    df_l_tot_return_index.columns = ['date', 'symbol', 'return']
    df_l_tot_return_index = df_l_tot_return_index.sort_values('date')
    
    merged = df_l_portfolio_wt
    original = df_l_tot_return_index
    df_temp_portfolio_wt = pd.merge(merged,original,how = 'left', on = ['symbol','date'])
    df_temp_portfolio_wt['temp'] = df_temp_portfolio_wt['return']+1
    df_temp_portfolio_wt['cum_return'] = df_temp_portfolio_wt.groupby(['symbol'])['temp'].apply(lambda x: x.cumprod().shift(1))
    df_temp_portfolio_wt['fill_weight'] = df_temp_portfolio_wt.groupby(['symbol'])['weight'].transform(lambda x: x.ffill())
    df_temp_portfolio_wt['fill_ind'] = df_temp_portfolio_wt.groupby(['symbol'])['ind'].transform(lambda x: x.ffill())
    df_temp_portfolio_wt['final_weight'] = df_temp_portfolio_wt['fill_weight'].mul(df_temp_portfolio_wt['cum_return'])
    alldates = pd.to_datetime(original['date'].unique())  
    for i in alldates:
        cond = df_temp_portfolio_wt.date == i
        df_temp_portfolio_wt.final_weight[cond] = df_temp_portfolio_wt.weight[cond]  #fill the portfolio dates with original weight
    df_temp_portfolio_wt = df_temp_portfolio_wt.dropna(subset=['final_weight'])
    df_temp_portfolio_wt = df_temp_portfolio_wt[['date','symbol','fill_ind','final_weight']]
    df_temp_portfolio_wt.columns=['date','symbol','ind','weight']
    temp = df_temp_portfolio_wt[df_temp_portfolio_wt['date'].isin(alldates)]
    temp['cash']=1- temp.groupby(['date'])['weight'].transform(sum)
    df_temp_portfolio_wt = pd.merge(df_temp_portfolio_wt,temp[['symbol','date','cash']],how = 'left', on = ['symbol','date'])
    df_temp_portfolio_wt['cash']= df_temp_portfolio_wt.groupby(['symbol'])['cash'].transform(lambda x: x.ffill())  #consider cash effect
    df_temp_portfolio_wt['sum'] = df_temp_portfolio_wt.groupby(['date'])['weight'].transform(sum)
    df_temp_portfolio_wt['total'] = df_temp_portfolio_wt['sum']+df_temp_portfolio_wt['cash']
    df_temp_portfolio_wt['final_weight'] = df_temp_portfolio_wt['weight']/df_temp_portfolio_wt['total']    #normalization
    df_temp_portfolio_wt = df_temp_portfolio_wt[['date','symbol','ind','final_weight']]
    df_temp_portfolio_wt.columns=['date','symbol','ind','weight']
    return df_temp_portfolio_wt
