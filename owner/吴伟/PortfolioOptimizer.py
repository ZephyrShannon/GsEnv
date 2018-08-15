# <codecell>

import sys
import itertools
from cvxopt import matrix, solvers, spmatrix, sparse
from cvxopt.blas import dot
import numpy
import pandas as pd
import numpy as np
from datetime import datetime

solvers.options['show_progress'] = False


def PortfolioOptimizer(context,portfolio_return,covariance_matrix,lambda_sigma,dt_begin,dt_end):
    portfolio_return = x0.asMatrix()
    covariance_matrix = covariance_matrix.asColumnTab()
    covariance_matrix = covariance_matrix.set_index('date')
    covariance_matrix = covariance_matrix.fillna(0)
    noa = portfolio_return.shape[1]
    dt_range = covariance_matrix.index.unique()
    if dt_begin > dt_range[0]:
        dt_range = dt_range[dt_begin:]
    if dt_end < dt_range[-1]:
        dt_range = dt_range[:dt_end]

    df_opts_weight = pd.DataFrame(np.nan, index=dt_range, columns=portfolio_return.columns)
    for date in dt_range:
        P = matrix(lambda_sigma*covariance_matrix.loc[date,:].pivot(index='o1',columns='o2',values='value').values, tc='d')
        q = matrix(-portfolio_return.loc[date,:], tc='d')
        G = matrix(-np.eye(noa))
        h = matrix(-np.zeros((noa, 1)))
        A = matrix(1.0, (1, noa))
        b = matrix(1.0)
        sol = solvers.qp(P, q, G, h, A, b)
        df_opts_weight.loc[date,:] = np.array(sol['x'].T).astype(np.float64)

    return df_opts_weight
