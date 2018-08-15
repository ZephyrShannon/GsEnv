# <codecell>

import numpy as np
import pandas as pd

def max(context,factors):
    reduce(lambda x,y: get_max_val(x,y), factors)
    
    
def get_max_val(x, y):
    return max(x,y)
