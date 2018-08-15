# <codecell>

import numpy as np
import pandas as pd

def MissingProcess(context,X,isListstate):
    df_fexpo=X.asMatrix().T
    df_fexpo_fillna=df_fexpo.fillna(df_fexpo.mean(axis=0,skipna=True))
    df_islist=isListstate.asMatrix().T.reindex(index=df_fexpo_fillna.index,columns=df_fexpo_fillna.columns)
    df_final_return=(df_fexpo_fillna * df_islist).T
    return df_final_return

# <codecell>



# <codecell>


