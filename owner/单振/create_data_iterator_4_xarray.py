# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils

# <codecell>


def create_data_iterator_4_xarray(context,data ,axis ,index_name ,column_name):
    return gsUtils.create_xarray_iterator(data, axis, index_name, column_name)

# <codecell>

