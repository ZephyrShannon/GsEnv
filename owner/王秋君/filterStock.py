# <codecell>

from lib.gftTools import gftIO
import numpy as np
import pandas as pd
def filterStock(context,x0,benchmark):
    benchmark=benchmark.asMatrix()
    ls_benchmark_date=benchmark.index
    df_ret=x0.asMatrix()
    ls_union_date = np.intersect1d(list(df_ret.index),list(ls_benchmark_date))
    df_retfilter=df_ret.reindex(index=ls_union_date)
    ls_ret=[pd.DataFrame(data=df_retfilter.ix[i].reindex(benchmark.ix[i].dropna().index.values)).rename(columns={i:'ret'}).assign(date=i) for i in ls_union_date]
    df_ret_pre=pd.concat(ls_ret,axis=0).reset_index()
    return df_ret_pre   
