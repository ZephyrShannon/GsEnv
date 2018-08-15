# <codecell>

import pandas as pd
import numpy as np


def get_one_industry_and_reindex(industry_info ,reindex_to ,industry_gid):
    if isinstance(reindex_to, gftIO.GftTable):
        reindex_to = reindex_to.matrix
    def_ind = gftIO.gid_str_to_bin(industry_gid)
    industry_index = industry_info['industry_idx']
    ind_idx = industry_index[industry_index['O1'] == def_ind].iloc[0]['idx']
    industry_data = industry_info['industry_data']
    industry_data = industry_data.reindex(index=reindex_to.index, columns=reindex_to.columns)
    industry_data = industry_data.fillna(method='ffill',axis=0)
    industry_data_c = industry_data.copy()
    industry_data_c[industry_data != ind_idx] = 0.0
    industry_data_c[industry_data.isnull()] = np.NaN
    industry_data_c[industry_data == ind_idx] = 1.0
    return industry_data_c


# <codecell>

