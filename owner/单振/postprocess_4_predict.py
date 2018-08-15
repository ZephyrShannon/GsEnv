# <codecell>

from lib.gftTools import gsUtils
import pandas as pd
import numpy as np

# <codecell>


def postprocess_4_predict(raw_datas ,na_droped ,it_ret):
    if isinstance(it_ret, gsUtils.SkipRow):
        it_ret = np.nan
    return pd.DataFrame(data=it_ret, index=na_droped.index, columns=['y_hat']).reindex(index=raw_datas.index)


# <codecell>

