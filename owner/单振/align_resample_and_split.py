# <codecell>

import numpy as np
import pandas as pd

def sample_choice_and_split(context,split_type,axis,intersect_set,args,sample):
    raise Exception("To be implemented")

# ##BEGIN AUTO CREATE CODE##
def get_desc_generator():
    return gsMeta.DescGenerator.create_default()
# end

# ##END AUTO CREATE CODE ##

# ##BEGIN CODES FOR CREATE_LAMBDA##
def create_func_lambda():
    # None for context, if function don't have context, remove it.
    return lambda split_type, axis, target_set, args, sample_freq: sample_select_and_split(None, split_type, axis, target_set, args, sample_freq)


def create_closure(split_type, axis, target_set, args, sample_freq):
    return gftIO.GsClosure('1CA7DE0E915A4C3BB2F28D9F11B40BCA', '790114F4DC6640A18C7BB555629EC49D', create_func_lambda(), split_type, axis, target_set, args, sample_freq)
# end 

# ##END CODES FOR CREATE_LAMBDA##
