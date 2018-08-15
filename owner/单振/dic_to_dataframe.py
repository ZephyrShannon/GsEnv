# <codecell>

import numpy as np
import pandas as pd

# <codecell>

from lib.gftTools import gsUtils


def dic_to_dataframe(axis ,dic_data):
    drop_na_df = list()
    drop_na_keys = list()
    while dic_data.has_next():
        val = dic_data.next()
        if  (val is not None) and (not isinstance(val, gsUtils.ItContinue)):
            drop_na_df.append(val)
            drop_na_keys.append(dic_data.key())
    if len(drop_na_df) > 0:
        ret = pd.concat(drop_na_df, axis=1)
        ret.columns = drop_na_keys
        ret = ret.transpose().reindex(dic_data.get_keys())
        if axis == 0:
            return ret
        else:
            return ret.transpose()
    else:
        raise Exception('No data available')


# <codecell>

