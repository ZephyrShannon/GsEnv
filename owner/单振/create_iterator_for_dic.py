# <codecell>

import numpy as np
import pandas as pd

# <codecell>

from lib.gftTools import gsUtils


def create_iterator_for_dic(context,dic_data):
    return gsUtils.DictIterator(dic_data)


# <codecell>

