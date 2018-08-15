# <codecell>

import numpy as np
import pandas as pd

def GetMEData(context,x):
    df_monthend_x=[(x[i][0],filter(x[i][1])) for i in range(len(x))]
    return df_monthend_x
def filter(data):
    df_x=data.asColumnTab()
    df_x['year'] = df_x['idname'].dt.year
    df_x['month'] = df_x['idname'].dt.month
    monthly_data = list(df_x.groupby(['year','month'])['idname'].max())
    final=df_x[df_x['idname'].isin(monthly_data)].drop(['year','month'],axis=1)
    return final

# <codecell>



# <codecell>



# <codecell>


