# <codecell>

import numpy as np
import pandas as pd
from datetime import date

def ExtractDateDiff(context,x):
    x = x.asColumnTab()
    x.dropna(inplace=True)
    column_type= gftIO.get_columns_type_dict(x)
    for key in column_type:
        if column_type[key]==2:
            x.rename(columns={key:'date'}, inplace=True)
        elif column_type[key]==4:
            x.rename(columns={key:'symbol'}, inplace=True)
        elif column_type[key]==23:
            x.rename(columns={key:'value'}, inplace=True)
    today = date.today()
    benchmarkDiff = (today - date(1800, 1, 1)).days
    x['value'] = benchmarkDiff - x['value']
    result = x
    return result
