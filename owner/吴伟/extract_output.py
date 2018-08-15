# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools.gsUtils import ExtractDictModelData as Extract


def extract_output(context,model,post_fix,oset_idx):
    output = Extract(model)
    return output.get_output(post_fix)    
