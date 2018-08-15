# <codecell>

# -*- coding: utf-8 -*-
import pandas as pd

# this function will move into gsUtils. put it here for test only.

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

def join(dataframe_1 ,dataframe_2 ,how ,left_on ,right_on ,select):
    """
Merge DataFrame objects by performing a database-style join operation by
columns or indexes.

If joining columns on columns, the DataFrame indexes *will be
ignored*. Otherwise if joining indexes on indexes or indexes on a column or
columns, the index will be passed on.

    Parameters
    ----------
    dataframe_1: O1T1V1   #index count start from 1
    dataframe_2: O1T1T2
    how : {'left', 'right', 'outer', 'inner'}, default 'inner'
    * left: use only keys from left frame, similar to a SQL left outer join;
      preserve key order
    * right: use only keys from right frame, similar to a SQL right outer join;
      preserve key order
    * outer: use union of keys from both frames, similar to a SQL full outer
      join; sort keys lexicographically
    * inner: use intersection of keys from both frames, similar to a SQL inner
      join; preserve the order of the left keys
    on : label or list
        Field names to join on. Must be found in both DataFrames. If on is
        None and not merging on indexes, then it merges on the intersection of
        the columns by default.
    left_on : label or list, or array-like
        Field names to join on in left DataFrame. Can be a vector or list of
        vectors of the length of the DataFrame to use a particular vector as
        the join key instead of columns
    right_on : label or list, or array-like
        Field names to join on in right DataFrame or vector/list of vectors per
        left_on docs
    select: return columns from the merged dataframe 

    """
    if isinstance(dataframe_1, gftIO.GftTable):
        otv_0 = dataframe_1.as_mutable_column_tab()
        otv_0 = otv_0.dropna()
    else:
        otv_0 = dataframe_1
    left_on_list = get_col_names_by_acronym(otv_0, left_on)

    if isinstance(dataframe_2, gftIO.GftTable):
        otv_1 = dataframe_2.as_mutable_column_tab()
        otv_1 = otv_1.dropna()
    else:
        otv_1 = dataframe_2

    right_on_list = get_col_names_by_acronym(otv_1, right_on)
    df_merge = pd.merge(otv_0, otv_1, how=how, left_on=left_on_list, right_on=right_on_list)
    select_list = get_col_names_by_acronym(df_merge, select)
    return df_merge.loc[:, select_list]


# <codecell>

