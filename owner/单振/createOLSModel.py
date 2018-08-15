# <codecell>

import numpy as np
import pandas as pd
import statsmodels.api as sm


class TestModel:
    def __init__(self):
        self.name = "OLS"
        return
    
    def createModel(self, y, X):
        return sm.OLS(y,X)

def CreateOLSModel(context):
    return TestModel()
