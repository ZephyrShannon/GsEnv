# <codecell>

import numpy as np
import pandas as pd

def ExtractKeys(context,dicts):
    string = str()
    for i in dicts.keys():
        string = string+i
    return string
