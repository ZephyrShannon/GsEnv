# <codecell>

import numpy as np
import pandas as pd

def selected_columns(data,column_name):
    df = data.asColumnTab()
    columns = np.array([item for item in column_name.split(',') if column_name.strip()])
    if not(set(columns).issubset(df.columns)):
         raise ValueError ('selected columns name are not existed in indexes')
    result = df[columns]
    return result
