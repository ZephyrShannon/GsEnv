# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils

def Greater(context,x,y):
    input_infos = gsUtils.align_input(x, y)
    oper = input_infos[0].get_operation(input_infos[1])
    
    if oper.just_do:
        ret = oper.left_value > oper.right_value
        if isinstance(ret, pd.Series):
            god_gid = gsUtils.getSingleGodGid()
            return ret.to_frame(god_gid)*1.0
        return ret*1.0
    else:
        return oper.left_value.gt(oper.right_value, axis='index')*1.0
