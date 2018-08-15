# <codecell>

import numpy as np
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier

def AdaBoost_Classifier(context,df_x,df_y,winSize,winStep):
    _CLASSIFIER=AdaBoostClassifier()
    return gsUtils.classify(context, df_x, df_y, winSize, winStep, _CLASSIFIER)
