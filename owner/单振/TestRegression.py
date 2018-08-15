# <codecell>

import numpy as np
import pandas as pd

def TestRegression(context,model_factory):
    y = [1,2,3]
    x = [[1,2,3],[2,4,6],[3,6,9]]
    model = model_factory.createModel(y,x)
    model.fit()
    return 1
