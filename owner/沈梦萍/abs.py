# <codecell>

import numpy as np
import pandas as pd

def abs(context,data):
    inputs = data.asMatrix()
    result = pd.DataFrame.abs(inputs)
    return inputs
