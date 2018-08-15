# <codecell>

import numpy as np
import pandas as pd

def add_dict_name_prefix(context,prefix,dicts):
    dict_new={}
    prefix_upper = prefix.upper()
    for key, value in dicts.items():
        new_key = prefix_upper+'_'+key
        dict_new[new_key] = value
        
#     for keys in list(dicts.keys()):
#         new_key = prefix.upper()+'_'+keys
#         dict_new[new_key] = dicts.pop(keys)
    return dict_new


def get_desc_generator():
    from lib.gftTools import gsMeta
    
    
    class AddPrefixDescGen(gsMeta.DescGenerator):
        def __init__(self):
            gsMeta.DescGenerator.__init__(self)
            return

        def get_instr_desc(self, gid, input_list, inst_id=None):
            prefix_name = input_list[0].scalar.upper() # prefix_name_index = 0
            dic_data = input_list[1] # dic_data_index = 1
            kv_map = dict()
            for key, value in dic_data.kv_map.items():
                kv_map[prefix_name+"_"+key] = value

            return gsMeta.InstrInstanceDesc.create_dict_meta(gid, dic_data.min_t, dic_data.max_t, dic_data.min_j_gid, dic_data.max_j_gid, kv_map, input_list, inst_id)

        def need_slice_data(self):
            return False
    return AddPrefixDescGen()


# ##BEGIN CODES FOR CREATE_LAMBDA##

def get_func():
    return add_dict_name_prefix

def create_func_obj(prefix, dict):
    return gftIO.GsFuncObj('6A875CE2B92D445C99BDA29F79FC0938', 'BFC5471876424B34925392A2B40D9E3D', add_dict_name_prefix,  False, prefix, dict)
# end 
# ##END CODES FOR CREATE_LAMBDA##

