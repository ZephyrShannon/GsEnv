# <codecell>

import numpy as np
import pandas as pd

def lag(data,if_lead):
    df = data.asMatrix()
    if if_lead ==1:
        result = df.shift(1)
    else:
        result = df.shift(-1)
    return result
