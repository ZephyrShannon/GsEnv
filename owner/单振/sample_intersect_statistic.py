# <codecell>

import numpy as np
import pandas as pd
from functools import reduce

def sample_intersect_statistic(context, sample_type, samples):
    ret = dict()
    if 1 == sample_type:
        o_list = list()
        t_list = list()
        for arg in samples:
            if isinstance(arg, gftIO.GftTable):
                mt = arg.asMatrix()
                o_list.append(mt.columns)
                t_list.append(mt.index)
            elif isinstance(arg, pd.DataFrame) and gftIO.ismatrix(arg):
                o_list.append(arg.columns)
                t_list.append(arg.index)
            elif arg is not None:
                raise Exception("Data[{0}] has incorrect type:{1}.".format(str(context.input_gid_list[i]), str(type(arg))))
        o_set = reduce(lambda x,y: x.intersection(y), o_list)
        t_set = reduce(lambda x,y: x.intersection(y), t_list)
        ret['o_set'] = o_set
        ret['t_set'] = t_set
    else:
        raise Exception("Sample type({0}) not supported".format(str(sample_type)))
    
    return ret
    



