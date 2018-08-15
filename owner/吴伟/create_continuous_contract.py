# <codecell>

import numpy as np
import pandas as pd

def create_continuous_contract(context,contract_data):
    ''' parse contract data to get continuous price for each group.
    Parameters
    ----------
    contract_data: OOTTV
    contract name, contract code, date, settlement date, close price

    Returns
    -------
    continuous_price: DataFrame
    '''
    if isinstance(contract_data, gftIO.GftTable):
        data = contract_data.asColumnTab().copy()

    name = {'INNERCODE': 'contract_code', 'OPTIONCODE': 'contract_name',
            'SETTLEMENTDATE': 'settlement_date', 'ENDDATE': 'date',
            'CLOSEPRICE': 'close_price'}
    data.rename(columns=lambda x: name[x], inplace=True)
    # drop rows without settlement date.
    data.dropna(subset=['settlement_date'], inplace=True)
    continuous_price = pd.DataFrame()

    target = data['contract_name'].unique()

    for num_contract, contract in enumerate(target):
        target_data = data[data['contract_name'] == contract]
        target_expiry_dates = target_data[['contract_code', 'settlement_date']].\
            drop_duplicates().sort_values('settlement_date')
        target_expiry_dates.set_index('contract_code', inplace=True)
        target_expiry_dates = target_expiry_dates[target_expiry_dates.columns[0]]
        target_data = target_data.loc[:, [
            'date', 'contract_code', 'close_price']]
        contract_data = target_data.pivot(
            index='date', columns='contract_code', values='close_price')
        contract_dates = contract_data.index
        continuous_contract_price = pd.Series(np.ones(len(contract_dates)),
                                              index=contract_dates,
                                              name=contract)
        prev_date = contract_dates[0]
        # Loop through each contract and create the specific weightings for
        # each contract depending upon the rollover date and price adjusted method.
        # Here for backtesting, we use last trading day rollover and backward ratio price adjustment.
        target_data_with_datetimeindex = target_data.set_index('date')
        price_adjust_ratio = pd.Series(np.ones(len(target_expiry_dates)),
                                       index=target_expiry_dates.values,
                                       name='ratio')
        adjusted_price = pd.Series(index=contract_dates,
                                   name=contract)
        target_data_with_datetimeindex['close_price'].replace(to_replace=0,
                                                              method='bfill',
                                                              inplace=True)
        target_data_with_datetimeindex['close_price'].replace(to_replace=0,
                                                              method='pad',
                                                              inplace=True)
        # drop duplicated datetime rows
        target_data_with_datetimeindex = target_data_with_datetimeindex[~target_data_with_datetimeindex.index.duplicated()]
        for i, (item, ex_date) in enumerate(target_expiry_dates.iteritems()):
            if i < len(target_expiry_dates) - 1 \
               and ex_date < target_data_with_datetimeindex.index[-1]:
                idx_ex_date = target_data_with_datetimeindex.index.searchsorted(
                    ex_date)
                pre_ex_date = contract_dates[idx_ex_date - 1]
                # ex_date has no price data, move ex_date to next trading date.
                if ex_date not in target_data_with_datetimeindex.index and \
                   idx_ex_date + 1 < len(target_data_with_datetimeindex.index):
                    ex_date = contract_dates[idx_ex_date + 1]
                else:
                    continue
                price_adjust_ratio.loc[ex_date] = target_data_with_datetimeindex['close_price'].loc[ex_date] / \
                    target_data_with_datetimeindex['close_price'].loc[pre_ex_date]

        # to create adjusted_pricested price by the product of target price date and
        # adjustment ratio.
        for i, (item, ex_date) in enumerate(target_expiry_dates.iteritems()):
            #print(i, item, ex_date)
            idx_ex_date = contract_data.index.searchsorted(ex_date)
            pre_ex_date = contract_dates[idx_ex_date - 1]
            adjusted_price.ix[prev_date:pre_ex_date] = target_data_with_datetimeindex['close_price'].ix[prev_date:pre_ex_date] * \
                price_adjust_ratio.ix[ex_date:].cumprod().iloc[-1]
            prev_date = ex_date
        continuous_price = pd.concat(
            [continuous_price, adjusted_price], axis=1)

    return continuous_price.fillna(method='pad')

