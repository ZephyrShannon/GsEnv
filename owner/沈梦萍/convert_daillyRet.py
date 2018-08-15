# <codecell>

import numpy as np
import pandas as pd

def convert_daillyRet(price,freq):
    if freq in (0,10,11,50):
        raise ValueError('Does not support!Please choose other options')
    price = price.asMatrix()
    price = price.dropna(axis=1,how='all') #remove non-business days
    
    df = pd.DataFrame({'date':price.index})
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['week'] = df['date'].dt.week
    df['days'] = df['date'].dt.day
    df['quarter'] = df['date'].dt.quarter
    
    yearly_data = df.groupby(['year'])['date'].max()
    monthly_data = df.groupby(['year','month'])['date'].max()
    quarterly_date = df.groupby(['year','quarter'])['date'].max()
    weekly_data = df.groupby(['year','month','week'])['date'].max()

    if freq == 20: #weekly
        result = weekly_data
    elif freq == 30:
        result =  monthly_data
    elif freq == 40:
        result= quarterly_date
    elif freq == 60:
        result =  yearly_data

    chosen_days = pd.DatetimeIndex(result)
    chosen_price = price.reindex(chosen_days)
    tot_return_index = chosen_price.pct_change(1)
    df_l_tot_return_index =  gftIO.convertMatrix2ColumnTab(tot_return_index)
    df_l_tot_return_index = df_l_tot_return_index.dropna()
    if len(df_l_tot_return_index.columns) ==2:
        column_type= gftIO.get_columns_type_dict(df_l_tot_return_index)
        for key in column_type:
            if column_type[key]==2:
                df_l_tot_return_index.rename(columns={key:'date'}, inplace=True)
            elif column_type[key]==23:
                df_l_tot_return_index.rename(columns={key:'ret'}, inplace=True)
    if len(df_l_tot_return_index.columns) ==3:
        column_type= gftIO.get_columns_type_dict(df_l_tot_return_index)
        for key in column_type:
            if column_type[key]==2:
                df_l_tot_return_index.rename(columns={key:'date'}, inplace=True)
            elif column_type[key]==23:
                df_l_tot_return_index.rename(columns={key:'ret'}, inplace=True)
            elif column_type[key]==4:
                df_l_tot_return_index.rename(columns={key:'symbol'}, inplace=True)
    result = df_l_tot_return_index.sort_values('date')
    return result
