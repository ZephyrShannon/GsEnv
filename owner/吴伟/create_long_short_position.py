# <codecell>

import numpy as np
import pandas as pd

def create_long_short_position(context,contract_data):
    """ create long short position, rolling over at the day before expiry date.
    """
    if isinstance(contract_data, gftIO.GftTable):
        data = contract_data.asColumnTab().copy()

    name = {
        'INNERCODE': 'contract_code',
        'OPTIONCODE': 'contract_name',
        'SETTLEMENTDATE': 'settlement_date',
        'ENDDATE': 'date',
        'CLOSEPRICE': 'close_price'
    }
    data.rename(columns=lambda x: name[x], inplace=True)
    data.dropna(subset=['settlement_date'], inplace=True)

    target = data['contract_name'].unique()
    roll_position = pd.DataFrame()
    # loop each commodity
    for num_contract, contract in enumerate(target):
        # print('contract name is %s', contract)
        target_data = data[data['contract_name'] == contract]
        target_expiry_dates = target_data[['contract_code', 'settlement_date']].\
            drop_duplicates().sort_values('settlement_date')
        target_expiry_dates.set_index('contract_code', inplace=True)
        target_expiry_dates = target_expiry_dates[target_expiry_dates.columns[
            0]]
        target_data = target_data.loc[:,
                                      ['date', 'contract_code', 'close_price']]
        contract_data = target_data.pivot(
            index='date', columns='contract_code', values='close_price')
        contract_dates = contract_data.index

        prev_date = contract_dates[0]
        # Loop through each contract and create the specific weightings for
        # each contract depending upon the rollover date and price adjusted method.
        # Here for backtesting, we use last trading day rollover and backward
        # ratio price adjustment.
        contract_roll_position = pd.DataFrame(
            np.zeros((len(contract_dates), len(target_data['contract_code'].unique()))),
            index=contract_dates,
            columns=target_data['contract_code'].unique())


        for i, (item, ex_date) in enumerate(target_expiry_dates.iteritems()):
            # ylog.info(item)
            # print(i, item, ex_date)
            if i < len(target_expiry_dates) - 1:
                idx_pre_ex_date = contract_data.index.searchsorted(ex_date)
                pre_ex_date = contract_dates[idx_pre_ex_date - 1]
                contract_roll_position.loc[prev_date:pre_ex_date, item] = 1
                idx_ex_item = pd.Index(target_expiry_dates).get_loc(ex_date)
                # ylog.info(idx_ex_item)
                # ylog.info(ex_date)
                if i < (len(target_expiry_dates) - 2):
                    far_item = target_expiry_dates.index[idx_ex_item + 1]
                    contract_roll_position.loc[prev_date:pre_ex_date, far_item] = -1
                # ylog.info('far month %s', far_item)
            else:
                contract_roll_position.loc[prev_date:, item] = 1
            prev_date = ex_date
        roll_position = pd.concat([roll_position, contract_roll_position], axis=1)

    return roll_position
