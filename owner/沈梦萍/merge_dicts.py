# <codecell>

import numpy as np
import pandas as pd

def merge_dicts(context,dict1,dict2):
    new_dicts = {**dict1, **dict2}
    return new_dicts





def get_desc_generator():
    
    from lib.gftTools import gsMeta

    class MergeDictsDescGen(gsMeta.DescGenerator):
        def __init__(self):
            gsMeta.DescGenerator.__init__(self)
            return

        def get_instr_desc(self, gid, input_list, inst_id=None):
            if input_list[0] is not None:
                # the 3rd input should be key value maps.
                kv_map = input_list[0].kv_map.copy()
            else:
                kv_map = None

            if input_list[1] is not None:
                if kv_map is None:
                    kv_map = input_list[1].kv_map.copy()
                else:
                    for key, value in input_list[1].kv_map.items():
                        kv_map[key] = value

            min_t, max_t, min_j_gid, max_j_gid = gsMeta.get_max_min_t_and_min_max_t(input_list)

            return gsMeta.InstrInstanceDesc.create_dict_meta(gid, min_t, max_t, min_j_gid, max_j_gid, kv_map, input_list, inst_id)

        def need_slice_data(self):
            return False
    return MergeDictsDescGen()

# ##BEGIN CODES FOR CREATE_LAMBDA##

def get_func():
    return merge_dicts

def create_func_obj(dict1, dict2):
    return gftIO.GsFuncObj('6A875CE2B92D445C99BDA29F79FC0938', '49EFD5C6530545618490610BE4103358', merge_dicts,  False, dict1, dict2)
# end 
# ##END CODES FOR CREATE_LAMBDA##

