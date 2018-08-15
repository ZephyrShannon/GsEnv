# <codecell>

import numpy as np
import pandas as pd

def calcumRet(ret):
    df = ret.asMatrix()
    result = df.cumsum(axis=0)
    return result
