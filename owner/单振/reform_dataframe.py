# <codecell>

import pandas as pd


def create_dataframe(data ,df):
    if isinstance(data, gsUtils.SkipRow):
        data = np.nan
    ret = pd.DataFrame(data=data, index= df.index, columns=df.columns)
    return ret


# <codecell>

