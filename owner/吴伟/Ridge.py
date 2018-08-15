# <codecell>

import numpy as np
import pandas as pd
from sklearn import linear_model
def Ridge(context,alpha,fit_intercept,normalize,copy_X,max_iter,tol,solver,random_state):
    return linear_model.Ridge(alpha,fit_intercept,normalize,copy_X,max_iter,tol,solver,random_state)
