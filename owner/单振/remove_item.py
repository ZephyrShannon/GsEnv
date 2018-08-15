# <codecell>

import numpy as np
import pandas as pd

# <codecell>

def remove_item(context,dic_data ,remove_key):
    ret = dict()
    for key, value in dic_data.items():
        if key != remove_key:
            ret[key] = value
    return ret


# <codecell>

