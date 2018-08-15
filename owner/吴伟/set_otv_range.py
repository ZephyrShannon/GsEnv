# <codecell>

import numpy as np
import pandas as pd



# set boundary vector for h
def set_upper_limit(x, multiplier):
    if x>= 0:
        return x*(1 + multiplier)
    else:
        return x*(1 - multiplier)


def set_lower_limit(x, multiplier):
    if x >= 0:
        return x*(1 - multiplier)
    else:
        return x*(1 + multiplier)
    
    
def set_otv_range(context,otv,value1_percentage,value2_percentage,oset_idx):
    """ set otv value to otvv by percentage range, value1_percentage is 1 which means set lower value to 0.
    """
    if isinstance(otv, gftIO.GftTable):
        otvv = otv.asColumnTab().copy()
        otvv.columns = ['date', 'target', 'value']
    
    if isinstance(oset_idx, gftIO.GftTable):
        gid = oset_idx.asColumnTab().iloc[:,0].values
    else:
        # select oset_idx rows
        gid = gftIO.strSet2Np(np.array(oset_idx))
    otvv = otvv.loc[otvv.target.isin(gid)]
    otvv.set_index('date', inplace=True)    
    otvv['value1'] = otvv['value'].apply(lambda x: set_lower_limit(x, value1_percentage))
    otvv['value2'] = otvv['value'].apply(lambda x: set_upper_limit(x, value2_percentage))
    
    otvv.drop(labels='value', axis=1, inplace=True)
    
    return otvv.reset_index()
