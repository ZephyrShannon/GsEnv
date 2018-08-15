# <codecell>

import numpy as np
import pandas as pd

def addString(context,val):
    return val.__str__()
# ##BEGIN AUTO CREATE CODE##

def get_desc_generator():
    from lib.gftTools import gsMeta
    class ReturnFirstDescGen(gsMeta.DescGenerator):
        def __init__(self):
            gsMeta.DescGenerator.__init__(self)
            return

        def get_instr_desc(self, gid, input_list, inst_id=None):
            return input_list[0]
            
        def need_slice_data(self):
            return False
    return ReturnFirstDescGen()
# end
# ##END AUTO CREATE CODE ##

# ##BEGIN CODES FOR CREATE_LAMBDA##

def get_func():
    return addString

def create_func_obj(val):
    return gftIO.GsFuncObj('1CA7DE0E915A4C3BB2F28D9F11B40BCA', '60CC97F9B58841A8A9FF81888628C680', addString,  False, val)
# end 
# ##END CODES FOR CREATE_LAMBDA##

