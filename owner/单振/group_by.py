# <codecell>

import pandas as pd
import numpy as np

def get_columns_type_4_otv(col_table: pd.DataFrame):
    ret = {'O':list(),'T':list(),'V':list()}
    for name in col_table.columns:
        type = gftIO.get_column_type(col_table, name)
        if type == gftIO.PARAMETER_TYPE_TIMESTAMP:
            ret['T'].append(name)
        elif type == gftIO.PARAMETER_TYPE_NUMBER_NUMRIC:
            ret['V'].append(name)
        elif type == gftIO.PARAMETER_TYPE_UUID:
            ret['O'].append(name)
    return ret

def get_col_names_by_acronym(col_table, col_names):
    otv_colmnes = get_columns_type_4_otv(col_table)
    by_name_list = list()
    col_names_list = col_names.split(',')
    for colname in col_names_list:
        idx = int(colname[1:]) - 1
        by_name_list.append(otv_colmnes[colname[0]][idx])
    return by_name_list

def group_by(column_tab_df ,by_columns: str,agg_func: str):
    if isinstance(column_tab_df, gftIO.GftTable):
        column_tab_df = column_tab_df.as_mutable_column_tab()

    by_name_list = get_col_names_by_acronym(column_tab_df, by_columns)
    return column_tab_df.groupby(by_name_list).agg(agg_func).reset_index()


# <codecell>

