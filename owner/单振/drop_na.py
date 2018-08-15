# <codecell>

import numpy as np
import pandas as pd

# <codecell>



def drop_na(axis ,how , *tables):
    axis = int(axis)
    df_list = list()
    for table in tables:
        if isinstance(table, gftIO.GftTable):
            if table.matrix is not None:
                df_list.append(table.matrix)
            else:
                df_list.append(table.columnTab)
        else:
            df_list.append(table)

    if axis == 1:
        merge_axis = 0
    else:
        merge_axis = 1
    if len(df_list) == 1:
        return df_list[0].dropna(axis=axis, how=how)
    
    merged = pd.concat(df_list, axis=merge_axis, join='inner')

    na_droped = merged.dropna(axis=axis, how=how)
    ret_list = list()
    if merge_axis == 1:
        for df in df_list:
            ret_list.append(na_droped[df.columns])
    else:
        for df in df_list:
            ret_list.append(na_droped.iloc[df.index])
    return ret_list


# <codecell>

