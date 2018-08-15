# <codecell>

import numpy as np
import pandas as pd

def extract_item(dic_data, name):
    return dic_data[name]
# ##BEGIN AUTO CREATE CODE##

def get_desc_generator():
    return gsMeta.DescGenerator.create_default()
# end

# ##END AUTO CREATE CODE ##

# ##BEGIN CODES FOR CREATE_LAMBDA##

def get_func():
    return extract_item

def create_func_obj(dic_data, name):
    return gftIO.GsFuncObj('1CA7DE0E915A4C3BB2F28D9F11B40BCA', '644B536C68664171A241A6D27C33E2B5', extract_item,  False, dic_data, name)
# end 

# ##END CODES FOR CREATE_LAMBDA##

