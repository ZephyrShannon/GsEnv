# <codecell>

import numpy as np
import pandas as pd
import math as mt
def calc_factor_ret_spe(context,df_specific_risk,half_life):
    #preprocessing
    half_life=int(half_life)
    df_specific_risk=df_specific_risk.asMatrix()
    ls_date = df_specific_risk.index.tolist()       ##date list
    
    #ls_symb_name = df_specific_risk.columns.tolist() ##fac_name list
    
    # get a date list for loop
    if len(ls_date) < half_life:
        raise Exception("More data needed")
        

    else:
        ls_date_for_loop = ls_date[half_life-1:len(ls_date)]
    specificwgts = list(
                map(
                        lambda x:mt.sqrt(0.5**(x/half_life)),  ## \sqrt{0.5^{x/halflife=4}}
                        list(range(half_life-1, -1, -1)) ) )
    # get a dict {time stamp: df}, df.index=symb, value= spec return var
    dict_retspec={}
    for date in ls_date_for_loop:

        df_ret_spec_slice = df_specific_risk[df_specific_risk.index <= date][-half_life:]
        df_retspec_var=df_ret_spec_slice.apply(lambda x: np.array(x) * np.array(specificwgts)).var()         
        dict_retspec[date]=df_retspec_var 
        
    return dict_retspec
