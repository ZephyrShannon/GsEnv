# <codecell>

# your code here
import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessClassifier

def GaussianProcess(context,df_x,df_y,winSize,winStep):
    _CLASSIFIER=GaussianProcessClassifier()
    return gsUtils.classify(context,df_x, df_y, winSize, winStep, _CLASSIFIER)

