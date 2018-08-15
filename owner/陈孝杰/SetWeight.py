# <codecell>

import numpy as np
import pandas as pd
from numpy import nan as NA

def SetWeight(pool,weight):
    df_pool = pool.asMatrix().copy()
    df_weight = weight.asMatrix().copy()
    df_weight = df_weight.reindex(df_pool.index, df_pool.columns, fill_value=NA)
    df_weight = df_weight * df_pool / df_pool
    df_weight = (df_weight.T / df_weight.sum(1)).T
    return df_weight
