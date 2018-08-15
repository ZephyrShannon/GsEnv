# <codecell>

import numpy as np
import pandas as pd

# <codecell>


import copy

def call_model_and_extract_info(model_fuc ,cleaned_data_in_list):
    if cleaned_data_in_list is not None:
        ret = model_fuc(*cleaned_data_in_list)
        return copy.deepcopy(ret)
    else:
        ret = None
    return ret


# <codecell>

