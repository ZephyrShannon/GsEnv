# <codecell>

import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB

def GaussionNB_Classifier(context,df_x,df_y,winSize,winStep):
    _CLASSIFIER=GaussianNB()
    return gsUtils.classify(context,df_x, df_y, winSize, winStep, _CLASSIFIER)
