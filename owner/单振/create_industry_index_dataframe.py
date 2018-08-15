# <codecell>

import pandas as pd
import numpy as np


def create_industry_index_dataframe(industry, ipo):
    if isinstance(industry, gftIO.GftTable):
        industry = industry.as_column_tab()
    if isinstance(ipo, gftIO.GftTable):
        ipo = ipo.as_column_tab()

    industry = industry.copy(False)
    ipo = ipo.copy(False)
    industry.columns=['O0','O1','T0','V0']
    all_industry = industry['O1'].unique()
    industry_index = np.array([float(i+1) for i in range(all_industry.__len__())])
    industry_index_df = pd.DataFrame(data=industry_index, columns=['idx'])
    all_industry_df = pd.DataFrame(data=all_industry, columns=['O1'])
    industry_index = pd.concat([all_industry_df, industry_index_df],axis=1)
    ind_matrix = industry.join(industry_index.set_index('O1'),on='O1',how='left')[['O0','T0','idx']]
    ind_mat = gftIO.convertColumnTabl2Matrix(ind_matrix)
    ipo['ISSUEPRICE'] = 0.0
    ipo_mat = gftIO.convertColumnTabl2Matrix(ipo)

    date_union = ind_mat.index.union(ipo_mat.index)
    symbol_intersect = ind_mat.columns.intersection(ipo_mat.columns)

    aligned_and_filled_ind = ind_mat.reindex(index=date_union,columns=symbol_intersect).fillna(method='ffill',axis=0).fillna(method='bfill',axis=0)

    aligned_and_filled_ipo = ipo_mat.reindex(index=date_union,columns=symbol_intersect).fillna(axis=0,method='ffill')
    merged_industry_data = aligned_and_filled_ind + aligned_and_filled_ipo
    # col_data = gftIO.convertMatrix2ColumnTabWithName(merged_industry_data, 'industry')
    # as_col_data = col_data[col_data['value'].notnull()]
    # as_col_data.columns = ['T0','O0','idx']
    # col_data_joined = as_col_data.join(industry_index.set_index('idx'),on='idx',how='left')[['O0','O1','T0','idx']]
    ret = dict()
    ret['industry_idx'] = industry_index
    ret['industry_data'] = merged_industry_data
    return ret


# <codecell>



def get_desc_generator():
    class IndustryIndexDFDescGen(gsMeta.DescGenerator):
        def __init__(self):
            gsMeta.DescGenerator.__init__(self)
            return

        def need_slice_data(self):
            return False
    
    return IndustryIndexDFDescGen()



# <codecell>

# cautions: if your function has lookback, probably there would be problems in deducing begin/end times for meta.
# ##BEGIN CODES FOR CREATE_LAMBDA##

def get_func():
    return create_industry_index_dataframe

def create_func_obj(industry_data, ipo_data):
    return gftIO.GsFuncObj('1CA7DE0E915A4C3BB2F28D9F11B40BCA', '1F19D05835664296BD56954F21A879B8', create_industry_index_dataframe,  False, industry_data, ipo_data)
# end 

# ##END CODES FOR CREATE_LAMBDA##
