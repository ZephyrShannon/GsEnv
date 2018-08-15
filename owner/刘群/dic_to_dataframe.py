# <codecell>

import pandas as pd

def dic_to_dataframe(data,date):
    df = data[date]
    df['y'] = df['close'].pct_change().fillna(0)
    df['y'] = np.exp(df['y'])
    return df


# <codecell>

