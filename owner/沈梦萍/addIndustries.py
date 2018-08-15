# <codecell>

import numpy as np
import pandas as pd

def addIndustries(df_l_src,df_l_industries):
    '''
      add industries info to src
      ---parameter---
      df_l_src: dataframe or gfttable
      industries: gfttable, ootv
    '''
    if isinstance(df_l_src,gftIO.GftTable):
            df_l_src = df_l_src.asColumnTab().copy()
            column_type= gftIO.get_columns_type_dict(df_l_src)
            for key in column_type:
                if column_type[key]==2:
                    df_l_src.rename(columns={key:'date'}, inplace=True)
                elif column_type[key]==4:
                    df_l_src.rename(columns={key:'symbol'}, inplace=True)
                elif column_type[key]==23:
                    df_l_src.rename(columns={key:'value'}, inplace=True)
            df_l_src.dropna(axis=0, how='any', inplace=True)

    if isinstance(df_l_industries, gftIO.GftTable):
        df_l_industries = df_l_industries.asColumnTab().copy()
        column_type= gftIO.get_columns_type_dict(df_l_industries)
        columns = []
        for key in column_type:
            if column_type[key]==2:
                df_l_industries.rename(columns={key:'date'}, inplace=True)
            elif column_type[key]==23:
                df_l_industries.rename(columns={key:'flag'}, inplace=True)
            elif column_type[key]==4: 
                columns.append(key)
        df_l_industries.rename(columns={columns[0]:'symbol'}, inplace=True)
        df_l_industries.rename(columns={columns[1]:'industry'}, inplace=True)
        df_l_industries.dropna(axis=0, how='any', inplace=True)
    
    if "flag" in df_l_industries.columns: 
            # just include values greater than 0 for 'df_l_industries' 
        df_l_industries = df_l_industries.query("flag > 0") 
        df_l_industries.drop("flag",axis=1, inplace=True)

    # align date range  
    if "date" in df_l_src.columns: 
        max_date = df_l_src.date.max()
        min_date = df_l_src.date.min()
        df_l_src = df_l_src.query("date>=@min_date & date<=@max_date")
        if "date" in df_l_industries.columns: 
            df_l_industries = df_l_industries.query("date>=@min_date & date<=@max_date")

    # merge
    df_l_src = pd.merge(df_l_src, df_l_industries, 
                              on=["date","symbol"],how="left")
    df_l_src.dropna(inplace=True)
    return df_l_src


