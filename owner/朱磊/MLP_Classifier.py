# <codecell>

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier

def MLP_Classifier(context,df_x,df_y,winSize,winStep):
    _CLASSIFIER=MLPClassifier()
    return gsUtils.classify(context, df_x, df_y, winSize, winStep, _CLASSIFIER)
