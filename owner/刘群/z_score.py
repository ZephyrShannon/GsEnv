# <codecell>

from scipy import stats
import pandas as pd

# <codecell>


def z_score(factor_dic):
    date_ls = list(factor_dic.keys())
    for date in date_ls:
        df = factor_dic[date].copy()
        arr = stats.zscore(factor_dic[date],axis=1)
        factor_dic[date]=pd.DataFrame(arr, index = df.index, columns = df.columns)
    return factor_dic

# get [2727 rows x 4 columns] for each date
# in other brunch cleaned stocks are (89, 2766)

# <codecell>

