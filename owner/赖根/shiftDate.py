# <codecell>

# Your code goes here.
import pandas as pd
import numpy as np

def shiftDate(df, n=1):
    n = int(n)
    if isinstance(df,gftIO.GftTable):
        df = df.asColumnTab()
    if not isinstance(df,pd.DataFrame):
        raise TypeError("Parameter type is wrong!")
    if "variable" in df.columns:
        df = df.drop("variable",axis=1)
    date_column = _findDateColumn(df.columns)
    df.rename(columns={date_column:"date"},inplace=True)
    df = df.sort_values("date",ascending=True)
    df.date = df.date.shift(n)
    df.dropna(inplace=True)
    return df

def _findDateColumn(ls_columns):
    for acolumn in ls_columns:
        if acolumn.upper() in ["T","DATE","IDNAME"]:
            return acolumn
    raise ValueError("Date Column isnot found in {}!".format(ls_columns))


