# <codecell>

import pandas as pd
from lib.gftTools import gsUtils


def reindex(df ,index ,columns):
    if isinstance(index, pd.DataFrame):
        index = pd.index
    if isinstance(columns, pd.DataFrame):
        columns = columns.columns
    return df.reindex(index,columns)


# <codecell>

