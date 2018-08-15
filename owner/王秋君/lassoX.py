# <codecell>

import numpy as np
import pandas as pd
from datetime import datetime as dt
def LassoX(context,x):
    new=[(x[i][0],filter(x[i][1])) for i in range(len(x))]
    return new
def filter(data):
    temp=data.asColumnTab()
    temp['year'] = temp['idname'].dt.year
    temp['month'] = temp['idname'].dt.month
    monthly_data = list(temp.groupby(['year','month'])['idname'].max())
    final=temp[temp['idname'].isin(monthly_data)].drop(['year','month'],axis=1)
    return final

# <codecell>


