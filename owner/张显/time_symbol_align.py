# <codecell>


import numpy as np
import pandas as pd
from functools import reduce
def time_symbol_align(context, j, oset, tset):
    if isinstance(j, gftIO.GftTable):
        mtx = j.asMatrix()
    elif isinstance(j, pd.DataFrame) and gftIO.ismatrix(j):
        mtx = j
    return mtx.loc[tset, oset]
    
    

