# <codecell>

import numpy as np
import pandas as pd

def CreateSparseMatricePanel(context,ootv):
    """
    convert the asset industry column table to pandas panel.
    1. convert input ootv to column table.
    2. change value to 1, binary value is set for asset with industry.
    3. get unique datetime.
    4. pivot the column table on a day, creating panel using pivot tables.
    """
    assets_group = ootv.asColumnTab()
    assets_group['value'] = 1
    datetime_index = pd.DatetimeIndex(assets_group['date'].unique())
    assets_group = assets_group.set_index('date')
    panel_binary = pd.Panel({date: pd.DataFrame(pd.pivot_table(assets_group.loc[date],values='value',index=['symbol'],columns=['industry'],fill_value=0))
                             for date in datetime_index})
    
    return panel_binary
