# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils

def groupNeutralWithTargetFilter(df_l_signals,df_l_benchmark,totalBinNum,returnBinIdx):
    totalBinNum = int(totalBinNum)
    returnBinIdx = int(returnBinIdx)
    if isinstance(df_l_signals, gftIO.GftTable):
        df_l_signals = df_l_signals.asColumnTab()
                # => date,industry,signal,symbold
    if isinstance(df_l_benchmark, gftIO.GftTable):
        df_l_benchmark = df_l_benchmark.asColumnTab()
                # => date,industry,industryWeight
    df_l_signals = df_l_signals.copy()
    df_l_signals.columns = ['date', 'symbol', 'signal', 'industry']
    df_l_benchmark = df_l_benchmark.copy()

        # drop na
    df_l_signals.dropna(axis=0, inplace=True)
    df_l_benchmark.dropna(axis=0, inplace=True)

        # align date
    max_date = df_l_signals.date.max()
    min_date = df_l_signals.date.min()
    df_l_benchmark = df_l_benchmark.query(
            "date>=@min_date & date<=@max_date")

    # add benchmark industry weight to signals
    df_l_signals = df_l_signals.merge(df_l_benchmark,
                                      on=["date", "industry"],
                                      how="left", suffixes=["", "_benchmark"])

    # calculate binIndex for each signal
    gb_signals = df_l_signals.groupby(['date', 'industry']).signal
    df_l_signals['signalNum'] = gb_signals.transform(np.size)
    df_l_signals['binIdx'] = gb_signals.transform(gsUtils.cut2bin, totalBinNum,
                                                  ascending=False)

    df_normal_signals = df_l_signals[df_l_signals['signalNum'] >= totalBinNum]
    df_thin_signals = df_l_signals[df_l_signals['signalNum'] < totalBinNum]
    if len(df_thin_signals) > 0:
        # need to support multiple choice
        df_thin_signals = df_thin_signals.ix[np.repeat(df_thin_signals.index, np.where(
            df_thin_signals['binIdx'] == 1, totalBinNum + 1 - df_thin_signals['signalNum'], 1).astype(int))]
        df_thin_signals = df_thin_signals.copy()
        df_thin_signals.ix[df_thin_signals['binIdx'] > 1, 'binIdx'] = df_thin_signals[df_thin_signals[
            'binIdx'] > 1]['binIdx'] - df_thin_signals[df_thin_signals['binIdx'] > 1]['signalNum'] + totalBinNum
        df_thin_signals.ix[df_thin_signals['binIdx'] == 1, 'binIdx'] = df_thin_signals[
            df_thin_signals['binIdx'] == 1].groupby(['date', 'industry'])['binIdx'].cumsum()

    df_l_signals = df_normal_signals.append(df_thin_signals, ignore_index=True)
    df_l_signals['weight'] = df_l_signals['industryWeight'] / \
        df_l_signals.groupby(['date', 'binIdx', 'industry'])[
        'signal'].transform(np.size)

    df_result = df_l_signals.query("binIdx==@returnBinIdx")
    df_result = df_result.dropna()
    return df_result[["date", "symbol", "weight"]]

