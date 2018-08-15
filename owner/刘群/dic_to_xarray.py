# <codecell>

import xarray as xr


def dic_to_xarray(dictionary):
    variables = {k: xr.DataArray(v,dims=['date','symbol']) for k, v in x_dic.items()}
    combined = xr.Dataset(variables).to_array(dim='factor')
    return combined


# <codecell>

