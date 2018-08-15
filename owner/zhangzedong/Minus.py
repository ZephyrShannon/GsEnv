# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils
def Minus(otv1,otv2):
    input_infos = gsUtils.align_input(otv1, otv2)
    oper = input_infos[0].get_operation(input_infos[1])
    
    if oper.just_do:
        if oper.order_changed:
            ret = oper.right_value - oper.left_value
        else:
            ret = oper.left_value - oper.right_value
        if isinstance(ret, pd.Series):
            god_gid = gsUtils.getSingleGodGid()
            return ret.to_frame(god_gid)
        return ret
    else:
        if oper.order_changed:
            oper.left_value = -oper.left_value
        else:
            oper.right_value = -oper.right_value
        # x - y = x + (-y) || y - x = y + (-x)
        return oper.left_value.add(oper.right_value, axis='index')
