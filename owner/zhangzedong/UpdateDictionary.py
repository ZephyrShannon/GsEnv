# <codecell>

import numpy as np
import pandas as pd

def UpdateDictionary(name,otv,dic):
    if dic is None:
        new_dic = {name:otv}
    else:
        tmp_tic = {name:otv}
        new_dic = dict(dic, **tmp_tic)
    return new_dic

# <codecell>


