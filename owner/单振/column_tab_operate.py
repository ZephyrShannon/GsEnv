# <codecell>

import numpy as np
import pandas as pd



def column_tab_operate(operation,col_data):
    if isinstance(col_data, gftIO.GftTable):
        data = col_data.columnTab.copy()
    else:
        data = col_data.copy()
    rename_map = rename_col_names(data)
    data.eval(operation, inplace=True)
    data.rename(columns=rename_map, inplace=True)
    return data

def rename_col_names(data: pd.DataFrame):
    rename_map = dict()
    new_columns = list()
    o_count = 0
    t_count = 0
    v_count = 0
    for colname in data.columns:
        col_type = gftIO.get_column_type(data, colname)
        if col_type == gftIO.PARAMETER_TYPE_NUMBER_NUMRIC:
            new_name = 'V{0}'.format(str(v_count))
            rename_map[new_name] = colname
            new_columns.append(new_name)
            v_count += 1
        elif col_type == gftIO.PARAMETER_TYPE_UUID:
            new_name = 'O{0}'.format(str(o_count))
            rename_map[new_name] = colname
            new_columns.append(new_name)
            o_count += 1
        else:  # T
            new_name = 'T{0}'.format(str(t_count))
            rename_map[new_name] = colname
            new_columns.append(new_name)
            t_count += 1
    data.columns = new_columns
    return rename_map


