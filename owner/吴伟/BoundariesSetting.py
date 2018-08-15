# <codecell>

import numpy as np
import pandas as pd

def BoundariesSetting(context,targets,default_lower_bnd,default_upper_bnd,user_input):
    if default_lower_bnd > default_upper_bnd:
        raise ValueError('default lower boundary value is greater than upper boundary value.')
    if isinstance(targets, gftIO.GftTable):
        df_target_limit = x0.asColumnTab()
    
    df_boundary = pd.DataFrame(columns=['date', 'target', 'lower_bnd', 'upper_bnd'])
    df_boundary['date'] = df_target_limit['idname']
    df_boundary['target'] = df_target_limit['variable']
    df_boundary['lower_bnd'] = default_lower_bnd
    df_boundary['upper_bnd'] = default_upper_bnd

    if user_input is not None:
        df_user_input_limit = x3.copy()
        df_user_input_limit = df_user_input_limit.set_index('variable')
        df_boundary = df_boundary.set_index('target')
        df_boundary.loc[df_user_input_limit.index, 'lower_bnd'] = df_user_input_limit['lower_bnd']
        df_boundary.loc[df_user_input_limit.index, 'upper_bnd'] = df_user_input_limit['upper_bnd']
        df_boundary.reset_index(inplace=True)
        
    return gftIO.GftTable(matrix=None, columnTab=df_boundary, matrixIsFromPython=True, gid='E3EA150B28B7417F99395788EB2C7E78', columnOrders=None)
