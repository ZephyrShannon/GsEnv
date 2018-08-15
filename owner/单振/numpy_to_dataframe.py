# <codecell>

import numpy as np
import pandas as pd

# <codecell>

from lib.gftTools import gsUtils


def reform_dataframe_with_one_col(data ,data_index ,column_name):
    if isinstance(data, gsUtils.ItContinue):
        data = np.nan
    if isinstance(data_index, pd.DataFrame):
        data_index = data_index.index
    if column_name is None:
        column_name = 'column'

    ret = pd.DataFrame(data=data, index= data_index, columns=[column_name])
    return ret


# <codecell>

