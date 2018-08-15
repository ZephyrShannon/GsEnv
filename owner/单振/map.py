# <codecell>

import numpy as np
import pandas as pd

# <codecell>

def map(context, func ,dic_data):
    ret = dict()
    for key, value in dic_data.items():
        ret[key] = func(value)
    return ret

# <codecell>

