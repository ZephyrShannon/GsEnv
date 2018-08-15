# <codecell>

import numpy as np
import pandas as pd

# <codecell>


import copy

def postprocess_4_model_fit(raw_datas ,preprocessed_datas ,ret):
    if ret is not None:
        return copy.deepcopy(ret)
    return ret


# <codecell>

