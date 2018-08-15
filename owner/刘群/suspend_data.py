# <codecell>

import pandas as pd


def suspend_data(data):
    df_dropna = data.asColumnTab().dropna()
    df_group_0 = df_dropna.groupby('value').get_group(0)
    groups = df_group_0.groupby('variable', squeeze=True)
    dic = {}
    for name, group in groups:
        dic[name] = group['idname']
    
    df = pd.DataFrame(dic)
    
    return df


# <codecell>

