# <codecell>

import numpy as np
import pandas as pd

def calcCumRet(context,singlePeriodRet):
    singlePeriodRet = singlePeriodRet.asMatrix()
    if len(singlePeriodRet) < 1:
        return type(singlePeriodRet)([])
    
    df_cum = (singlePeriodRet + 1).cumprod(axis=0) - 1
    
    return df_cum
