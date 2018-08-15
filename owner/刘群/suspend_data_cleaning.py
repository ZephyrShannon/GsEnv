# <codecell>

import pandas as pd

def suspend_data_cleaning(data):
    df_dropna = data.asColumnTab().dropna()
    df_group_0 = df_dropna.groupby('value').get_group(0)
    groups = df_group_0.groupby('variable', squeeze=True)
    
    dic ={}
    
    for name, group in groups:
        dic[name] = group.idname.iloc[-1]
    return dic


# <codecell>

