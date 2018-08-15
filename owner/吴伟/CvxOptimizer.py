# <codecell>

# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import re
import itertools

from cvxopt import matrix, solvers, spmatrix, sparse
from cvxopt.blas import dot

from lib.gftTools import gsConst
# import U_PNL_FITNESS as fitness

solvers.options['show_progress'] = False


def logrels(rets):
    """Log of return relatives, ln(1+r), for a given DataFrame rets."""
    return np.log(rets + 1)


def check_boundary_constraint(df_asset_bound, df_group_bound,
                              df_exposure_bound, df_exposure):
    ''' check input boundary limit.

    Parameters
    ----------
    df_asset_bound : dataframe-like
        Input lower and upper boundary dataframe for each asset.

    df_group_bound : dataframe-like
        Input lower and upper boundary dataframe for each group.

    df_exposure_bound : dataframe-like
        Input lower and upper boundary dataframe for each factor.

    df_exposure : dataframe
        Big X.

    Returns
    -------
    True: all boundaries in condition.
    False: any boundaries out of condition.
    '''
    if ((df_asset_bound.lower) < 0).any():
        raise ValueError('short is not supported.')
    if ((df_asset_bound.upper) > 1).any():
        raise ValueError('asset upper boundary is bigger than 1.')
    if (np.sum(df_asset_bound.lower) > 1):
        raise ValueError('asset lower boundary sum is bigger than 1.')
    if (np.sum(df_asset_bound.upper) < 1):
        raise ValueError('asset upper boundary sum is smaller than 1.')
    if ((df_asset_bound.lower > df_asset_bound.upper).any()):
        raise ValueError('asset lower boundary is bigger than upper boundary')

    if ((df_group_bound.lower) < 0).any():
        raise ValueError('short is not supported.')
    if ((df_group_bound.upper) > 1).any():
        raise ValueError('group upper boundary is bigger than 1.')
    if (np.sum(df_group_bound.lower) > 1):
        raise ValueError('group lower boundary sum is bigger than 1.')
    if (np.sum(df_group_bound.upper) < 1):
        raise ValueError('group upper boundary sum is smaller than 1.')
    if ((df_group_bound.lower > df_group_bound.upper).any()):
        raise ValueError('group lower boundary is bigger than upper boundary')

    df_factor_exposure_bound_check = pd.DataFrame(index=df_exposure.T.index, columns=[['lower', 'upper']])
    df_factor_exposure_bound_check.lower = df_exposure.T.min(axis=1)
    df_factor_exposure_bound_check.upper = df_exposure.T.max(axis=1)

    if (df_factor_exposure_bound_check.upper < df_exposure_bound.upper).any():
        raise ValueError('factor exposure upper setting error')

    if (df_factor_exposure_bound_check.lower > df_exposure_bound.lower).any():
        raise ValueError('factor exposure lower setting error')

    return True


def statistics(weights, rets, covariance):
    """Compute expected portfolio statistics from individual asset returns.

    Parameters
    ----------
    rets : DataFrame
        Individual asset returns.  Use numeral rather than decimal form
    weights : array-like
        Individual asset weights, nx1 vector.

    Returns
    -------
    list of (pret, pvol, pstd); these are *per-period* figures (not annualized)
        pret : expected portfolio return
        pvol : expected portfolio variance
        psr  : sharpe ratio

    """

    if isinstance(weights, (tuple, list)):
        weights = np.array(weights)
    
    if isinstance(weights, matrix):
        df_single_return = rets.values * weights.T
        df_single_return = pd.DataFrame(df_single_return, index=rets.index)
        df_single_return = df_single_return.sum(axis=1)
        pret = np.sum(logrels(rets.values).mean() * weights)
        pvol = np.dot(weights.T, np.dot(covariance, weights))
    elif isinstance(weights, pd.DataFrame):
        #df_single_return = pd.DataFrame(rets.values * np.array(weights).T, index=rets.index).sum(axis=1)
        #pret = np.sum(logrels(rets.values).mean() * weights.T)
        pret = np.dot(weights.values, logrels(rets).mean())
        pvol = np.dot(weights, np.dot(covariance, weights.T))
        #asset_return.dot(np.array(df_pivot_industries_asset_weights).T).sum()
    pstd = np.sqrt(pvol)
    #psr = sharpe_ratio(df_single_return, 0)
    #pret2 = np.sum(logrels(rets.values).mean() * weights.values)
    return [pret, pvol, pret/pstd]


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
            raise KeyError('invalid input date: %s' % date)
    factor_exposure.columns = gftIO.strSet2Np(factor_exposure.columns.values)
    factor_exposure = factor_exposure.fillna(0)

    return factor_exposure


def find_nearest(array, value):
    if isinstance(array, list):
        array = np.array(array)
        idx = (np.abs(array-value)).argmin()
    return idx



def CVXOptimizer(context, target_mode, position_limit, risk_model,
                 asset_return, asset_weight, target_risk, target_return,
                 target_date):
    """
    optimize fund weight target on different constraints, objective, based on
    target type and mode, fund return target, fund weight, group weight， etc.

    Parameters
    ----------
    target_date: Timestamp
        Specific date.

    target_mode: dictionary
        target optimization type({type: mode})
        0: minimum risk.
        1: minimum risk subject to target return.
        2: maximum return subject to target risk.

    asset_return: Dataframe, OTV,
        asset return for all symbols.
        index=date, O: asset names, V: asset return.

    risk model: dictionary
        Risk factor exposure: DataFrame
            所有股票在因子上暴露的值，p.s. 如有8个因子，就有8个DataFrame,
            得把所有8个因子某一天所有值先取出来得到一个n*k的矩阵.n为股票，k为因子
        Specific Risk: DataFrame
            用来组成对角矩阵Delta.

    asset_weight: Dataframe, OOTV
        T=date, O: asset names, O: group names, V: asset weight.
        weight bound of each asset. Default is equal weight.

    target_return: double
        Target return for portfolio respected to benchmark.

    target_risk: double
        Portfolio risk tolerance whose objective is maximum return.

    Returns:
    ----------
    df_result: DataFrame
        Optimized value of weight.
        Index: target date.
        Columns: assets names.

    """
    asset_return = asset_return.asMatrix()
    asset_weights = asset_weight.asColumnTab()
    target_date = pd.to_datetime(target_date)

    # regex to search all the factors
    ls_factor = [x[:-4] for x in risk_model.keys() if re.search(".ret$", x)]
    # ls_factor = [x.split('.')[0] for x in ls_factor]

    specific_risk = risk_model['specificRisk'].pivot(
        index='date', columns='symbol', values='specificrisk')
    target_date = pd.datetime(year=2016, month=10, day=31)
    target_return = -0.00096377
    target_risk = 3.16026352e-06
    target_mode = 0
    position_limit = 500

    # find the nearest date next to target date from specific risk
    dt_next_to_target = specific_risk.index.searchsorted(target_date)
    dt_next_to_target = specific_risk.index[dt_next_to_target]
    target_specific_risk = specific_risk.loc[dt_next_to_target, :]

    # drop duplicated rows at date
    df_industries_asset_weight = asset_weights.drop_duplicates(
        subset=['date', 'symbol'])
    try:
        df_industries_asset_init_weight = df_industries_asset_weight[
            df_industries_asset_weight['date'] == target_date].dropna()
    except KeyError:
        raise KeyError('invalid input date: %s' % target_date)

    # drop incomplete rows
    df_industries_asset_init_weight = df_industries_asset_init_weight.dropna(
        axis=0, subset=['industry', 'symbol'], how='any')

    # find intersection symbol between risk model and initial weight
    # try:
    #     df_industries_asset_init_weight = df_industries_asset_init_weight.sample(position_limit)
    # except ValueError:
    #     print("position limit is bigger than total symbols")
    unique_symbol = df_industries_asset_init_weight['symbol'].unique()
    target_symbols = target_specific_risk.index.intersection(unique_symbol)
    if position_limit > len(target_symbols):
        print("position limit is bigger than total symbols")
        position_limit = len(target_symbols)

    arr = list(range(len(target_symbols)))
    np.random.shuffle(arr)
    target_symbols = target_symbols[arr[:position_limit]]

    df_industries_asset_target_init_weight = df_industries_asset_init_weight.\
                                             loc[df_industries_asset_init_weight['symbol'].isin(target_symbols)]
    df_pivot_industries_asset_weights = pd.pivot_table(
        df_industries_asset_target_init_weight, values='value', index=['date'],
        columns=['industry', 'symbol'])
    df_pivot_industries_asset_weights = df_pivot_industries_asset_weights.fillna(0)
    # idx = pd.IndexSlice

    noa = len(target_symbols)
    if noa < 1:
        print("no intersected symbols from specific risk and initial holding.")

    idx_level_1_value = df_pivot_industries_asset_weights.columns.get_level_values(1)
    asset_return = asset_return.loc[:target_date, idx_level_1_value].fillna(0)

    diag = specific_risk.loc[dt_next_to_target, target_symbols]
    delta = pd.DataFrame(np.diag(diag), index=diag.index,
                         columns=diag.index).fillna(0)

    big_X = get_factor_exposure(risk_model, ls_factor, target_date,
                                target_symbols)
    big_X = big_X.fillna(0)
    all_factors = big_X.columns

    covariance_matrix = risk_model['ret_cov'].set_index('date')

    cov_matrix = covariance_matrix.loc[dt_next_to_target]
    cov_matrix = cov_matrix.pivot(index='factorid1', columns='factorid2',
                                  values='value')
    cov_matrix = cov_matrix.reindex(all_factors, all_factors, fill_value=np.nan)

    cov_matrix_V = big_X.dot(cov_matrix).dot(big_X.T) + delta

    P = matrix(cov_matrix_V.values)
    q = matrix(np.zeros((noa, 1)), tc='d')

    A = matrix(1.0, (1, noa))
    b = matrix(1.0)

    # for group weight constraint
    groups = df_pivot_industries_asset_weights.groupby(
        axis=1, level=0, sort=False, group_keys=False).count().\
        iloc[-1, :].values
    num_group = len(groups)
    num_asset = np.sum(groups)
    # target mode 1, b_asset and b_group are supposed to be a DataFrame
    #b_asset = tuple((0.0, 1.0) for i in asset_return.columns)
    #b_group = [(0.0, 1.0)] * num_group
    df_asset_weight = pd.DataFrame({'lower': [0.0], 'upper': [1.0]},
                                   index=target_symbols)

    df_group_weight = pd.DataFrame({'lower': [0.0], 'upper': [1.0]},
                                   index=set(idx_level_0_value))


    df_factor_exposure_bound = pd.DataFrame(index=big_X.T.index, columns=[['lower', 'upper']])
    df_factor_exposure_bound.lower = (1.0/n)*big_X.sum()*(0.999991)
    df_factor_exposure_bound.upper = (1.0/n)*big_X.sum()*(1.000009)
    df_asset_bnd_matrix = matrix(np.concatenate(((df_asset_weight.upper, df_asset_weight.lower)), 0))
    df_group_bnd_matrix = matrix(np.concatenate(((df_group_weight.upper, df_group_weight.lower)), 0))
    
    df_factor_exposure_bound_check = pd.DataFrame(index=big_X.T.index, columns=[['lower', 'upper']])
    df_factor_exposure_bound_check.lower = big_X.T.min(axis=1)
    df_factor_exposure_bound_check.upper = big_X.T.max(axis=1)
    if check_boundary_constraint(df_asset_weight, df_group_weight, df_factor_exposure_bound, big_X):
        print("constraint setting is OK")
    
    #position_limit = noa
    #arr = np.array([1] * position_limit + [0] * (noa-position_limit))
    #np.random.shuffle(arr)

    rets_mean = logrels(asset_return).mean()
    avg_ret = matrix(rets_mean.values)
    G = matrix(-np.transpose(np.array(avg_ret)))
    # G = matrix(-np.transpose(np.array(avg_ret)))
    h = matrix(-np.ones((1, 1))*target_return)
    G_sparse_list = []
    for i in range(num_group):
        for j in range(groups[i]):
            G_sparse_list.append(i)
    Group_sub = spmatrix(1.0, G_sparse_list, range(num_asset))

    asset_sub = matrix(np.eye(noa))
    # asset_sub = matrix(np.eye(n))
    # exp_sub = matrix(np.array(big_X.T))
    exp_sub = matrix(np.array(big_X.T))

    G = matrix(sparse([G, asset_sub, -asset_sub, Group_sub, -Group_sub,
                       exp_sub, -exp_sub]))

    b_asset_upper_bound = np.array([x[-1] for x in b_asset])
    b_asset_lower_bound = np.array([x[0] for x in b_asset])
    b_asset_matrix = matrix(np.concatenate((b_asset_upper_bound,
                                            -b_asset_lower_bound), 0))
    b_group_upper_bound = np.array([x[-1] for x in b_group])
    b_group_lower_bound = np.array([x[0] for x in b_group])
    b_group_matrix = matrix(np.concatenate((b_group_upper_bound,
                                            -b_group_lower_bound), 0))
    b_factor_exposure = list(zip((big_X*(1.0/n)).sum()*(0.9991), (big_X*(1.0/n)).sum()*1.0001))
    b_factor_exposure_upper_bound = np.array([x[-1] for x in b_factor_exposure])
    b_factor_exposure_lower_bound = np.array([x[0] for x in b_factor_exposure])
    b_factor_exposure_matrix = matrix(np.concatenate(
        (b_factor_exposure_upper_bound, -b_factor_exposure_lower_bound), 0))

    h = matrix(sparse([h, b_asset_matrix, b_group_matrix,
                       b_factor_exposure_matrix]))

    if target_mode == 0:
        G = matrix(-np.eye(noa), tc='d')
        h = matrix(-np.zeros((noa, 1)), tc='d')
        sol = solvers.qp(P, q, G, h, A, b)
        df_opts_weight = pd.DataFrame(np.array(sol['x']).T,
                                      columns=target_symbols,
                                      index=[target_date])
    elif target_mode == 1:
        sol = solvers.qp(P, q, G, h, A, b)
        df_opts_weight = pd.DataFrame(np.array(sol['x']).T,
                                      columns=target_symbols,
                                      index=[target_date])
    elif target_mode == 2:
        N = 1000
        mus = [10**(5.0*t/N-0.0) for t in range(N)]
        G = matrix(sparse([asset_sub, -asset_sub, Group_sub, -Group_sub,
                           exp_sub, -exp_sub]))
        h = matrix(sparse([b_asset_matrix, b_group_matrix,
                           b_factor_exposure_matrix]))
        xs = [solvers.qp(mu*P, q, G, h, A, b)['x', 'status'] for mu in mus]
        # returns = [dot(matrix(logrels(asset_return).mean()).T, x['x'])
        #           for x in xs]
        risk = [dot(x['x'], P*x['x']) for x in xs]

        target_risk_index = find_nearest(risk, target_risk)
        df_opts_weight = pd.DataFrame(np.array(xs[target_risk_index]).T,
                                      columns=target_symbols,
                                      index=[target_date])
        sol['status'] = xs[target_risk_index]['status']

    if sol['status'] == 'optimal':
        print('result is optimal')
        return df_opts_weight
    elif sol['status'] == 'unknown':
        raise('the algorithm failed to find a solution that satisfies the specified tolerances')
        #raise("")

    #return df_opts_weight

