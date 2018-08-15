# <codecell>

import numpy as np
import pandas as pd
import statsmodels.api as sm

class RLMModel:
    def __init__(self, arg):
        self.arg = arg
    
    def fit(self, X, y):
        model = sm.RLM(y, X, M=sm.robust.norms.HuberT())
        return model.fit()
    
    def __getstate__(self):
        attr_dict = self.__dict__.copy()
        return attr_dict
    
    
def create_RLM_model(context,M):
    return RLMModel(M)
