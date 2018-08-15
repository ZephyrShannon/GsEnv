# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gftIO
import xarray as xr
from functools import reduce
import timeit
import binascii


def risk_model_preprocess(industry_factor_expos, style_factor_expos, market_cap, ret_factor):
    data_all_cols = list()
    data_all_index = list()
    for data in industry_factor_expos.values():
        data_all_cols.append(data.asMatrix().columns)
        data_all_index.append(data.asMatrix().index)
    for data in style_factor_expos.values():
        data_all_cols.append(data.asMatrix().columns)
        data_all_index.append(data.asMatrix().index)

    market_cap_df = market_cap.asMatrix()
    ret_factor_shifted_df = ret_factor.asMatrix().shift(-1)
    data_all_cols.append(market_cap_df.columns)
    data_all_index.append(market_cap_df.index)
    data_all_cols.append(ret_factor_shifted_df.columns)
    data_all_index.append(ret_factor_shifted_df.index)

    intersect_date = reduce(np.intersect1d, data_all_index)
    intersect_symbol = reduce(np.intersect1d, data_all_cols)

    all_ind_factors = dict()
    all_style_factors = dict()
    for key, value in industry_factor_expos.items():
        all_ind_factors[key] = value.asMatrix().reindex(intersect_date, intersect_symbol).fillna(axis=0,method='ffill')
    for key, value in style_factor_expos.items():
        all_style_factors[key] = value.asMatrix().reindex(intersect_date, intersect_symbol).fillna(axis=0,method='ffill')

    ret_and_weight_dict = dict()
    ret_gid_str = y_gid_str
    market_gid_str = weight_gid_str 
    ret_and_weight_dict[market_gid_str] = market_cap_df.reindex(intersect_date, intersect_symbol)
    ret_and_weight_dict[ret_gid_str] = ret_factor_shifted_df.reindex(intersect_date, intersect_symbol)

    ind_xr = create_x_array(all_ind_factors)
    style_xr = create_x_array(all_style_factors)
    ret_and_weight_xr = create_x_array(ret_and_weight_dict)

    ind_null_filter = ind_xr.notnull().all(axis=0)
    style_null_filter = style_xr.notnull().all(axis=0)
    sqrt_market_cap_null_filter = ret_and_weight_xr.notnull().all(axis=0)
    all_filter = sqrt_market_cap_null_filter  # & ind_null_filter #& style_null_filter

    ind_xr_weighted = ind_xr * ret_and_weight_xr.loc[market_gid_str, :, :]
    ind_xr_weighted_filtered = ind_xr_weighted * all_filter
    constrain = ind_xr_weighted_filtered.sum(dim='symbol')

    const_xr = xr.Dataset({constrain_bin_gid: constrain}).to_array(dim='symbol')
    ind_xr_weighted_with_constrain = xr.concat([ind_xr_weighted, const_xr], dim='symbol')

    style_constr_xr = create_xarray_with_value(constrain_bin_gid, 0., intersect_date, style_xr.factor.values, ['date','factor'], 'symbol')
    style_xr_add_constrain = xr.concat([style_xr, style_constr_xr], dim='symbol')

    ret_and_weight_constr_xr = create_xarray_with_value(constrain_bin_gid, 0., intersect_date, ret_and_weight_xr.factor.values, ['date', 'factor'], 'symbol')
    ret_and_weight_xr_add_constrain = xr.concat([ret_and_weight_xr, ret_and_weight_constr_xr], dim='symbol')

    country_xr = create_xarray_with_value(country_gid_str, 1., ret_and_weight_xr_add_constrain.date, ret_and_weight_xr_add_constrain.symbol, ['date','symbol'], 'factor')
    all_factor_concated = xr.concat([ind_xr_weighted_with_constrain, style_xr_add_constrain, country_xr], dim='factor')
    
    ret = dict()
    ret['X'] = all_factor_concated
    ret['y'] = ret_and_weight_xr_add_constrain.loc[ret_gid_str,:,:].to_pandas()
    return ret


def create_x_array(data_dict):
    variables = {k: xr.DataArray(v, dims=['date', 'symbol']) for k, v in data_dict.items()}
    combined = xr.Dataset(variables).to_array(dim='factor')
    return combined


def create_xarray_with_value(key, value, data_index, data_columns, data_dims, key_dim):
    zero_df = pd.DataFrame(value, index=data_index, columns=data_columns)
    variables = {key : xr.DataArray(zero_df, dims=data_dims)}
    return xr.Dataset(variables).to_array(dim=key_dim)


constrain_bin_gid = gftIO.gid_str_to_bin('B1ADFB044AA94F5F9EE8F945E47F87AD')
country_gid_str = 'E8A54A95C9264162BEEC88B9CF65C78B'
weight_gid_str = '07C1FF96E4EA49BE8DFA12B6CBAB289F'
y_gid_str = '925A3DAF6E954E4AAD405B3EBA03F675'
