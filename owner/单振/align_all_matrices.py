# <codecell>

import numpy as np
import pandas as pd
from functools import reduce


# <codecell>

def align_all_matrices(dic_data):
    dic_copy = dict()
    o_list = list()
    t_list = list()
    for key, data in dic_data.items():
        if isinstance(data, gftIO.GftTable):
            data = data.as_matrix()
            dic_copy[key] = data
            o_list.append(data.columns)
            t_list.append(data.index)
        elif isinstance(data, pd.DataFrame):
            o_list.append(data.columns)
            t_list.append(data.index)

    o_set = reduce(lambda x, y: x.intersection(y), o_list)
    t_set = reduce(lambda x, y: x.intersection(y), t_list)
    for key, data in dic_copy.items():
        dic_copy[key] = data.loc[t_set, o_set]
    return dic_copy


# <codecell>


def get_desc_generator():
    import copy
    class AlignAllMatricesDescGen(gsMeta.DescGenerator):
        def __init__(self):
            gsMeta.DescGenerator.__init__(self)
            return

        def need_slice_data(self):
            return False

        def get_instr_desc(self, gid, input_list, inst_id=None):
            dic_val = input_list[0]
            
            ret = copy.copy(dic_val.kv_map[list(dic_val.kv_map.keys())[0]])
            print("get meta of gid:" + str(ret.j_gid)+":"+str(ret))
            
            ret.j_gid = gid
            ret.inst_id = inst_id
            ret.input_list = input_list
            return ret
            
    return AlignAllMatricesDescGen()


# <codecell>

# cautions: if your function has lookback, probably there would be problems in deducing begin/end times for meta.
# ##BEGIN CODES FOR CREATE_LAMBDA##

def get_func():
    return align_all_matrices

def create_func_obj(datas):
    return gftIO.GsFuncObj('1CA7DE0E915A4C3BB2F28D9F11B40BCA', '6CE211EC173345D590E741344FEF5D38', align_all_matrices,  False, datas)
# end 



# ##END CODES FOR CREATE_LAMBDA##
