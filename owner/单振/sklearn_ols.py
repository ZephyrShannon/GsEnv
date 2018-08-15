# <codecell>

import numpy as np
import pandas as pd

# <codecell>

from sklearn.linear_model import LinearRegression


def sklearn_ols(context,X_set ,y ,weights):
    model = LinearRegression()
    model.fit(X,y)
    return model


# <codecell>

