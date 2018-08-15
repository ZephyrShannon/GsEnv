# <codecell>

import numpy as np
import pandas as pd


def get_factor_exposure(risk_model, factor_list, date, symbols):
    ''' Return factor exposure matrix(big X).

    Parameters
    ----------
    risk_model: dictionary
        Including specific risk, different factor exposure dataframe for all
        symbols.

    factor_list: list
        Factor exposure list.

    Returns
    -------
    factor_exposure: DataFrame
        Big X on target date for input symbols.
    '''
    factor_exposure = pd.DataFrame(index=symbols)
    for factor in factor_list:
        try:
            factor_exposure[factor] = risk_model[factor].asMatrix().\
                                      loc[date, symbols]
        except KeyError:
            factor_exposure[factor] = np.nan
            #raise KeyError('invalid input date: %s' % date)
    factor_exposure.columns = gftIO.strSet2Np(factor_exposure.columns.values)
    factor_exposure = factor_exposure.fillna(0)

    return factor_exposure

def FactorExposure(context,risk_model,begin_date,end_date,frequency,asset_weight,factors):
    '''to get benchmark factor exposure'''
    asset_weight = asset_weight.asMatrix()
    begin_date = pd.to_datetime(begin_date)
    end_date = pd.to_datetime(end_date)
    
    # resample to monthly data
    if frequency == 'MONTHLY':
        m = benchmark_weight.index.to_period('m')
        asset_weight = asset_weight.reset_index().groupby(m).last().set_index('index')
        asset_weight.index.name = ''
        asset_weight = asset_weight.loc[begin_date:end_date]
    if isinstance(factors, dict):
        factors = factors['factors']
    risk_model_exposure = pd.Panel({target_date: get_factor_exposure(risk_model, factors, target_date,
                            benchmark_weight.columns).T for target_date in benchmark_weight.index})
    factor_exposure = pd.DataFrame(index=benchmark_weight.index, columns=risk_model_exposure.major_axis)
    for target_date in benchmark_weight.index:
        factor_exposure.ix[target_date] = risk_model_exposure.ix[target_date].dot(benchmark_weight.ix[target_date].fillna(0))
    return factor_exposure.replace(0, np.nan).fillna(method='ffill') 
