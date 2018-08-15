# <codecell>

import numpy as np
import pandas as pd

def CreateDiagonalMatricePanel(context,otv):
    """
    # 1. convert input otv to column table.
    # 2. select the datetime index from otv. 
    # 3. loop the datetime index to convert assets on that date to a diagonal matrix, creating a 3-d panel.

    """
    if isinstance(otv, gftIO.GftTable):
        assets = otv.asColumnTab()
        assets.columns = ['idname', 'variable', 'value']
    assets = assets.set_index('idname')
    datetime_index = assets.index.unique()
    
    panel_diag = pd.Panel({date: pd.DataFrame(np.eye(len(assets.loc[date,'variable'])), index=assets.loc[date,'variable'],
                                              columns=assets.loc[date,'variable']) for date in datetime_index})
    
    return panel_diag
