# <codecell>

import numpy as np
import pandas as pd

def CalcRet(context,x):
    price = x.asColumnTab()
    column_type= gftIO.get_columns_type_dict(price)
    for key in column_type:
        if column_type[key]==2:
            price.rename(columns={key:'date'}, inplace=True)
        elif column_type[key]==4:
            price.rename(columns={key:'symbol'}, inplace=True)

    price['ret'] = price.groupby('symbol').pct_change(1)
    price.dropna(inplace=True)
    ret = price[['symbol','date','ret']]
    
    return ret
