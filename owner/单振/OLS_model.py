# <codecell>

import numpy as np
import pandas as pd

# <codecell>

def OLS_model(context,X_array,y,args):
    model = sm.RLM(y, X_array, M=sm.robust.norms.HuberT())
    return model.fit()

# <codecell>

