# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils

def SVM(context,df_x,df_y,winSize,winStep,clf):
    return gsUtils.classify(context,df_x, df_y, winSize, winStep, clf)
