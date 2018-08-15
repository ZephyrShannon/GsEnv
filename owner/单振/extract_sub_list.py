# <codecell>

import numpy as np
import pandas as pd

# <codecell>

from lib.gftTools import gsUtils


def extract_sub_list(iterator, indexes_str):
    return gsUtils.create_extract_multi_values(iterator,indexes_str)


# <codecell>

