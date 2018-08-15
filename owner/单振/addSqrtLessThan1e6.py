# <codecell>

import numpy as np
import pandas as pd
import math
import time

def addSqrtLessThan1e6(x0,x1):
    time.sleep(100)
    ret = x0.asMatrix()
    ret += math.sqrt(x1)
    return ret

def precheck(context, x0, x1):
    if not isinstance(x0, gftIO.GftTable):
        raise Exception("x0 is not gftTable!")
    if isinstance(x1, int) or isinstance(x1, float):
        if x1 < 0:
            raise Exception("x1 is less than zero!")
        elif x1 > 1000000:
            raise Exception("x1 is too large!")
        else:
            return
    raise Exception("x1 is not float or int")
