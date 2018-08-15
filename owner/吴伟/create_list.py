# <codecell>

import numpy as np
import pandas as pd

def create_list(context,args):
    result = []
    for i in range(len(args)):
        result.append(args[i])
    return result        
