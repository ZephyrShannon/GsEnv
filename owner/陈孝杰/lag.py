# <codecell>

import numpy as np
import pandas as pd

def lag(context,x,period):
    result = x.asMatrix().copy()
    period = int(period)
    result = result.shift(period)
    return result
