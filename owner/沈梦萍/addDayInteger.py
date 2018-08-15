# <codecell>

import numpy as np
import pandas as pd

def addDayInteger(context,x):
    x = x0.asColumnTab()
    #rename column names
    column_type= gftIO.get_columns_type_dict(x)
    for key in column_type:
        if column_type[key]==2:
            x.rename(columns={key:'date'}, inplace=True)
    #transform dates
    date= x['date'].values
    dates = gftIO.transformTime4Output(date)
    original_dates = np.zeros(len(dates), dtype='datetime64[ns]')
    original = gftIO.transformTime4Output(original_dates)
    #calculate difference(62091 is the difference between 1800/01/01 and 1970/01/01)
    diff = np.array(dates - original+62091,dtype = np.float64)
    x['value'] = diff
    return x

