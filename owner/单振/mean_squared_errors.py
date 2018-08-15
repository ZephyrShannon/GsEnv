# <codecell>

import numpy as np
import pandas as pd

# <codecell>

from sklearn import metrics

def mean_squared_errors(y ,y_hat):
    its = y.index.intersection(y_hat.index)
    return metrics.mean_squared_error(y.loc[its], y_hat.loc[its])



# <codecell>

