# <codecell>

# Your code goes here.
import statsmodels.api as sm
import pandas as pd
import numpy as np
from numpy import nan as NA

def CS_OLS(Y,X):
    alldates = pd.to_datetime(np.intersect1d(X.index, Y.index))
    Y = Y.reindex(alldates, Y.columns, fill_value=NA)
    X = X.reindex(alldates, Y.columns, fill_value=NA)
    result = pd.DataFrame(NA, index=alldates, columns=Y.columns)
    for d in alldates:
        xd = X.ix[d].dropna()
        yd = Y.ix[d].dropna()
        allsyms = np.intersect1d(xd.axes, yd.axes)
        if len(allsyms) > 2:
            result.ix[d, allsyms] = sm.OLS(yd.ix[allsyms], xd.ix[allsyms]).fit().resid
    return result


