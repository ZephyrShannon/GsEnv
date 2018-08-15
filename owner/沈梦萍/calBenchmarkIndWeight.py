# <codecell>

import numpy as np
import pandas as pd

def calBenchmarkIndWeight(df_l_benchmark):
     '''
    calculate industry weight in benchmark
    ---parameter---
    df_l_benchmark: DataFrame(columns={"date","symbol","industry","weight"})
    '''
    # calculate industry weight
    if isinstance(df_l_benchmark, gftIO.GftTable):
        df_l_benchmark = df_l_benchmark.asColumnTab()
        df_l_benchmark.dropna(axis=0,inplace=True)
    df_l_benchmark = df_l_benchmark.copy()
    gb_l_benchmark = df_l_benchmark.groupby(['date','industry'])
    df_l_benchmark = gb_l_benchmark.weight.sum().to_frame("industryWeight").reset_index()
    
    return df_l_benchmark


