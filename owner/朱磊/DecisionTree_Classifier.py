# <codecell>

# your code here
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

def DecisionTree_Classifier(context,df_x,df_y,winSize,winStep):
    _CLASSIFIER=DecisionTreeClassifier()
    return gsUtils.classify(context, df_x, df_y, winSize, winStep, _CLASSIFIER)
