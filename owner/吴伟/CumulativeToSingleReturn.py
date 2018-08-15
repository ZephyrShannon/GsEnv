# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gftIO


def CumulativeToSingleReturn(context,df_cumulative_return):
    df_cumulative_return = df_cumulative_return.asMatrix()
    df_cumulative_return = df_cumulative_return.add(1)
    df_single_return = df_cumulative_return.div(df_cumulative_return.shift(1)) - 1
    #df_single_return.ix[0] = df_cumulative_return.ix[0] - 1
    return df_single_return    

# <codecell>


