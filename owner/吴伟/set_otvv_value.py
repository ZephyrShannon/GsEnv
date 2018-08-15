# <codecell>

import numpy as np
import pandas as pd


name = {2:'idname', 23:'value', 4:'variable'}


def set_otvv_value(context,otv,value1,value2,otvv):
    """ expand the otv to otvv with value1 and value2, then update this dataframe with input otvv.
    Parameters:
    otv: input portfolio OTV.
    otvv: user defined otvv value.
    """
    if value1 > value2:
        raise ValueError('default value1 is greater than value2.')
    if isinstance(otv, gftIO.GftTable):
        df_otv = otv.asColumnTab().copy()
        if isinstance(df_otv.index, pd.DatetimeIndex):
            df_otv.reset_index(inplace=True)
        
        # rename according to column value type
        df_otv.rename(columns=lambda x: name[(gftIO.get_column_type(df_otv,x))], inplace=True)
    if isinstance(otvv, gftIO.GftTable):
        otvv = otvv.asColumnTab().copy()
        
    df_otvv = pd.DataFrame(columns=['date', 'target', 'value1', 'value2'])
    df_otvv['date'] = df_otv['idname']
    df_otvv['target'] = df_otv['variable']
    df_otvv['value1'] = value1
    df_otvv['value2'] = value2

    if otvv is not None:
        df_otvv.update(otvv)
        
#    return gftIO.GftTable(matrix=None, columnTab=df_otvv, matrixIsFromPython=True, gid='E3EA150B28B7417F99395788EB2C7E78', columnOrders=None)
    return df_otvv
