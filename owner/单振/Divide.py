# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils
def Divide(otv1, otv2):
    otv1 = otv1.asMatrix()
    otv2 = otv2.asMatrix()
    try:
        common_index = np.intersect1d(otv1.index, otv2.index)
        otv1 = otv1.reindex(common_index)
        otv2 = otv2.reindex(common_index)
        col_num1 = len(otv1.columns)
        col_num2 = len(otv2.columns)
        if col_num1 == 1 and otv1.columns[0] == gsUtils.getGodGid() and col_num2 != 1:
            tmp = np.tile(otv1, col_num2)
            output = tmp/otv2
        elif col_num1 != 1 and col_num2 == 1 and otv2.columns[0] == gsUtils.getGodGid():
            tmp = np.tile(otv2, col_num1)
            output = otv1/tmp
        else:
            output = otv1/tmp
    except:
            output = otv1/otv2
    try:
        output = output.dropna(axis=[0,1], how='all')
    except:
        pass
    return output
