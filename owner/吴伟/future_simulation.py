# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gftIO, gsUtils, gsConst


def future_simulation(context,start_date,end_date,df_position,df_price,df_multiplier,df_commission,df_trading_volume):
    """
    
    """
    if isinstance(df_commission, gftIO.GftTable):
        df_commission = df_commission.asColumnTab().copy()
    if isinstance(df_position, gftIO.GftTable):
        df_position = df_position.asMatrix().copy()
    if isinstance(df_price, gftIO.GftTable):
        df_price = df_price.asColumnTab().copy()
    if isinstance(df_multiplier, gftIO.GftTable):
        df_multiplier = df_multiplier.asColumnTab().copy()
    df_price_name = {'INNERCODE': 'contract_code', 'OPTIONCODE': 'contract_name',
            'SETTLEMENTDATE': 'settlement_date', 'ENDDATE': 'date',
            'CLOSEPRICE': 'close_price'}
    df_price.rename(columns=lambda x: df_price_name[x], inplace=True)
    df_price = df_price.pivot(index='date', columns='contract_code', values='close_price')
    df_position.replace(to_replace=0, value=np.nan, inplace=True)
    df_position = df_position.loc[start_date:end_date]
    df_price = df_price.loc[start_date:end_date]
    # process multiplier
    df_multiplier_name = {
        'CONTRACTINNERCODE': 'contract_code',
        'CMVALUE': 'multiplier',
        'CTIME': 'date',
        'OPTIONCODE': 'contract_name'
    }

    df_multiplier.rename(columns=lambda x: df_multiplier_name[x], inplace=True)

    df_multiplier.dropna(subset=['multiplier'], inplace=True)
    ds_multiplier = df_multiplier.set_index('contract_code')['multiplier']
    
    # calculate value
    df_portfolio_value = df_position * df_price * ds_multiplier
    value = df_portfolio_value.sum(1)
    value = value.iloc[value.nonzero()]
    value = value.to_frame()
    value.columns = gsUtils.getCashGid()
    return value
