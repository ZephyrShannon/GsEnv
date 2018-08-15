# <codecell>

import numpy as np
import pandas as pd

def replace(context,ootv_1,ootv_2):
    if isinstance(ootv_1, gftIO.GftTable):
        ootv_1 = ootv_1.asColumnTab()
    if isinstance(ootv_2, gftIO.GftTable):
        ootv_2 = ootv_2.asColumnTab()
    if ootv_2 is not None:
        df_user_input_limit = user_input.copy()
        df_user_input_limit = df_user_input_limit.set_index('variable')
        df_boundary = df_boundary.set_index('target')
        df_boundary.loc[df_user_input_limit.index, 'lower_bnd'] = df_user_input_limit['lower_bnd']
        df_boundary.loc[df_user_input_limit.index, 'upper_bnd'] = df_user_input_limit['upper_bnd']
        df_boundary.reset_index(inplace=True)                
