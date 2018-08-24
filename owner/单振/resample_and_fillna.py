# <codecell>

from lib.gftTools import gftIO
import numpy as np
import pandas as pd



def resample_and_fillna(data,freq = None,lookback = None):
    if lookback is not None and (lookback < 0):
        lookback = None # -1 means None  # 0 mean no fillna
    if isinstance(data, pd.DataFrame):
        if gftIO.ismatrix(data):
            return resample_and_fill_na_matrix(data, freq, lookback)
        else:
            return resample_and_fill_na_col_tab(data, freq, lookback)
    else:
        raise Exception("Can not resample data of type:" + str(type(data)))


def resample_and_fill_na_matrix(mat: pd.DataFrame, freq, lookback):
    if lookback > mat.index.size:
        lookback = None

    if lookback == None:
        # fill the source first.
        mat = mat.fillna(axis=0, method='ffill')
        # than reindex it.
        return mat.reindex(freq,method='ffill')

    if freq is not None:
        if lookback <= 1:
            return mat.reindex(freq, method='ffill',limit=1)
        else:
            # fillna the remaining lookback - 1 period
            # see data in test2
            mat_reidx = mat.reindex(freq, method='ffill',limit=1)
            mat_reidx.fillna(method='ffill',limit=lookback-1, inplace=True)
            return mat_reidx
    else:
        return mat.fillna(axis=0, method='ffill',limit=lookback)

    

def resample_and_fill_na_col_tab(col_tab: pd.DataFrame, freq, lookback):
    # only one t and one v is allowed.
    tName = None
    vList = None
    oList = None

    for colName in col_tab.columns:
        if (col_tab[colName].dtype == np.float64):
            if vList is None:
                vList = list()
            vList.append(colName)
        elif gftIO.istimestamparray(col_tab[colName]):
            if tName is None:
                tName = colName
        else:
            if oList is None:
                oList = list()
            oList.append(colName)

    if tName is None:
        raise Exception("No T column found!")

    if vList is None:
        raise Exception('No V column is found!')

    multi_v = len(vList) > 1

    if multi_v:
        mat = col_tab.pivot_table(values=vList, index=tName, columns=oList)
    else:
        vName = vList[0]
        mat = col_tab.pivot_table(values=vName, index=tName, columns=oList)

    # mat = mat.fillna(axis=0, method='ffill', limit=1)
    old_freq_name = freq.name
    freq.name = tName
    mat = resample_and_fill_na_matrix(mat, freq, lookback)
    freq.name = old_freq_name
    mat.index.name = tName

    if multi_v:
        # stack oList back and reset index.
        stacked_mat = mat.stack(level=oList)
        stacked_mat.reset_index(inplace=True).dropna(how='all', subset=vList)
        ret = stacked_mat
    else:
        mat_reseted = mat.reset_index()
        ret = mat_reseted.melt(id_vars=tName, value_name=vName).dropna(how='any', subset=vList)
    return ret

    
def get_freq_index(freq):
    if isinstance(freq, pd.DatetimeIndex):
        return freq
    elif isinstance(freq, pd.DataFrame):
        if gftIO.ismatrix(freq):
            return freq.index
    raise Exception("Can not accept freq of type:" + str(type(freq)))


# use this to test OOTVV resample
def test_melt():
    pd_list = list()
    delta = pd.Timedelta('1D')
    pd1 = pd.Timestamp('2016-10-01')
    for i in range(9):
        pd_list.append(pd1)
        pd1 = pd1 + delta

    df = pd.DataFrame({"A": ["X1", "X1", "X1", "X2", "X2", "X2", "X3", "X3", "X3"],
                       "B": ["Y1", "Y2", "Y3", "Y1", "Y2", "Y3", "Y1", "Y2", "Y3"],
                       "C": pd_list, "D": [1., 2., 2., 3., 3., 4., 5., 6., 7.], 
                       "E": [9., 10., 11., 12., 13., 14., 15., 16., 17.]})

    pd_list_2 = list()
    delta = pd.Timedelta('2D')
    pd1 = pd.Timestamp('2016-10-01')
    for i in range(7):
        pd_list_2.append(pd1)
        pd1 = pd1 + delta
    freq = pd.DatetimeIndex(pd_list_2)
    col_tab = df

    return resample_and_fill_na_col_tab(df, freq, 2)


def test2():
    pd_list = list()

    pd1 = pd.Timestamp('2016-10-01')
    pd_list.append(pd1)
    pd1 = pd1 + pd.Timedelta('20D')
    # pd_list.append(pd1)
    delta = pd.Timedelta('2D')
    for i in range(8):
        pd_list.append(pd1)
        pd1 = pd1 + delta
    # 10 date.

    df = pd.DataFrame({"A": ["X1", "X1", "X1", "X2", "X2", "X2", "X3", "X3", "X3"],
                       # "B": ["Y1", "Y2", "Y3", "Y1", "Y2", "Y3", "Y1", "Y2", "Y3"],
                       "C": pd_list, "D":  [1., 2., 3., 4., 5., 6., 7., 8., 9.],
                       # "E": [9., 10., 11., 12., 13., 14., 15., 16., 17.]
                       })

    pd_list_2 = list()
    delta = pd.Timedelta('4D')
    pd1 = pd.Timestamp('2016-10-02')
    for i in range(15):
        pd_list_2.append(pd1)
        pd1 = pd1 + delta
    freq = pd.DatetimeIndex(pd_list_2)
    col_tab = df
    ret = resample_and_fill_na_col_tab(df, freq, 3)

# <codecell>

# codes here is for melt creation.

from lib.gftTools import gsMeta

