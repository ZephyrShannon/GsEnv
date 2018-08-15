# <codecell>

# Your code goes here.
import pandas as pd
import numpy as np

def mergeByDate(*ls_df):
    if len(ls_df)<1:
        raise ValueError("Input paramerter must have one dataframe at least!")
    df_result = ls_df[0]
    if isinstance(df_result,gftIO.GftTable):
        df_result = df_result.asColumnTab()
    if "variable" in df_result.columns:
        df_result = df_result.drop("variable",axis=1)
    date_column = _findDateColumn(df_result.columns)
    value_column = _findValueColumn(df_result.columns)
    df_result.rename(columns={date_column:"date",value_column:"x0"},
                     inplace = True)
    df_result.sort_values("date",inplace=True, ascending=True)
    for i in range(1,len(ls_df)):
        df = ls_df[i]
        if isinstance(df,gftIO.GftTable):
            df = df.asColumnTab()
        if "variable" in df.columns:
            df = df.drop("variable",axis=1)
        date_column = _findDateColumn(df.columns)
        value_column = _findValueColumn(df.columns)
        df.rename(columns={date_column:"date",value_column:"x"+str(i)},
                                  inplace = True)
        df.sort_values("date",inplace=True, ascending=True)
        df_result = pd.merge_ordered(df_result,df,on="date",how="outer")
    df_result.dropna(inplace=True)
    return df_result
    

def _findDateColumn(ls_columns):
    for acolumn in ls_columns:
        if acolumn.upper() in ["T","DATE","IDNAME"]:
            return acolumn
    raise ValueError("Date Column isnot found in {}!".format(ls_columns))
        
    
def _findValueColumn(ls_columns):
    for acolumn in ls_columns:
        if acolumn.upper() in ["VALUE","VAL","V"]:
            return acolumn
    raise ValueError("Value Column isnot found in {}!".format(ls_columns))

