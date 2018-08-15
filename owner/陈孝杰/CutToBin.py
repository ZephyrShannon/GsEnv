# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils

def CutToBin(signal,totalBinNum,returnBinIdx):
    totalBinNum = int(totalBinNum)
    returnBinIdx = int(returnBinIdx)
    df_pool = signal.asColumnTab().copy()
    
    #set the column name by column_type
    column_type= gftIO.get_columns_type_dict(df_pool)
    for key in column_type:
        if column_type[key]==2:
            df_pool.rename(columns={key:'date'}, inplace=True)
        elif column_type[key]==4:
            df_pool.rename(columns={key:'symbol'}, inplace=True)
        elif column_type[key]==23:
            df_pool.rename(columns={key:'sig'}, inplace=True)
    df_pool = df_pool.dropna(axis=0, how='any')   
    
    sig_grouped = df_pool.groupby(['date'])[['sig']]
    df_pool['signalNum'] =  sig_grouped.transform(np.size)
    df_pool['binIdx'] = sig_grouped.transform(gsUtils.cut2bin, totalBinNum, False)   
    
    df_normal_pool = df_pool[df_pool['signalNum']>=totalBinNum]
    df_thin_pool = df_pool[df_pool['signalNum']<totalBinNum]
    if len(df_thin_pool) > 0:
        df_thin_pool = df_thin_pool.ix[np.repeat(df_thin_pool.index, np.where(df_thin_pool['binIdx']==1, totalBinNum+1-df_thin_pool['signalNum'], 1))]
        df_thin_pool = df_thin_pool.copy()
        df_thin_pool.ix[df_thin_pool['binIdx']>1, 'binIdx'] = df_thin_pool[df_thin_pool['binIdx']>1]['binIdx']-df_thin_pool[df_thin_pool['binIdx']>1]['signalNum']+ totalBinNum
        df_thin_pool.ix[df_thin_pool['binIdx']==1, 'binIdx'] = df_thin_pool[df_thin_pool['binIdx']==1].groupby(['date'])['binIdx'].cumsum()

    df_pool = df_normal_pool.append(df_thin_pool, ignore_index=True)

    result = df_pool.ix[df_pool['binIdx']==returnBinIdx, ['date','symbol','sig']]    
    
    return result
