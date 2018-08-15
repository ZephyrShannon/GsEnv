# <codecell>

import numpy as np
import pandas as pd

def set_otv_value(context,otv,value):
    if isinstance(otv, gftIO.GftTable):
        otv = otv.asColumnTab()
        otv.value = value
        
    return otv
