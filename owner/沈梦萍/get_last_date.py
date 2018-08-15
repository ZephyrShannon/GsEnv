# <codecell>

import numpy as np
import pandas as pd

def get_last_date(context,data,n):
    data = data.asMatrix()
    n = int(n)
    new_data = data.dropna(how='all')
    dates = new_data.index
    if n>=len(dates):
        last_date = dates[0]
    else:
        last_date = dates[-n-1]
    return last_date

