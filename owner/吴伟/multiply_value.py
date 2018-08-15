# <codecell>

import numpy as np
import pandas as pd

def multiply_value(context,otv,value):
    """ change the value of otv to 1, then multiplying the input value
    """
    if isinstance(otv, gftIO.GftTable):
        otv = otv.asColumnTab()
    otv['value'] = 
