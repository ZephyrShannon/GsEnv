# <codecell>

import xarray as xr


def create_xarray(factor_dic):
    variables = {k: xr.DataArray(v,dims=['date','symbol']) for k, v in factor_dic.items()}
    combined = xr.Dataset(variables).to_array(dim='factor')
    return combined


# <codecell>

