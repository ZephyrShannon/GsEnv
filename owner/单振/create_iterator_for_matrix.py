# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils

# <codecell>

def create_iterator_for_matrix(data ,axis):
    if axis == 0 or axis is None:
        return gsUtils.create_index_iterator(data)
    return gsUtils.create_column_iterator(data)

# <codecell>

