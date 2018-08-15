# <codecell>

import numpy as np
import pandas as pd

def ShanzhenAdd(x0,x1):
    return x0.asMatrix() + x1

def precheck(context, x0, x1):
    if isinstance(x1, gftIO.GftTable):
        raise Exception("x1 is not gftTable")
