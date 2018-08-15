# <codecell>

import numpy as np
import pandas as pd

def foo(context,date,x):
    x = x.asMatrix()
    x = x + 1
    return x
