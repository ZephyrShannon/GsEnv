# <codecell>

import numpy as np
import pandas as pd

def OTVStandardlization(otv):
    mean = otv.mean(axis=1)
    std = otv.std(axis=1)
    output = ((otv.T - mean)/std).T
    output[np.isinf(output)] = np.nan
    return output
