# <codecell>

import numpy as np
import pandas as pd

# <codecell>



def drop_if_any_none(*datas):
    for data in datas:
        if data is None:
            return None
    return datas



# <codecell>

