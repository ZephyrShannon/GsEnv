# <codecell>

import numpy as np
import pandas as pd
from sklearn import linear_model
def Ridge_fit(context,RidgeModel,X,y,sample_weight):
    X=X.asMatrix()
    
    return RidgeModel.fit(X,y,sample_weight)
