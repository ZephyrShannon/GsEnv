# <codecell>


def stocks_filter_with_benchmark(stocks ,benchmark):
    benchmark=benchmark.asMatrix()
    benchmark_date=benchmark.index
    df_ret=stocks.asMatrix()
    intersection_date = df_ret.index.intersection(benchmark_date) 
    df_ret_date_filter=df_ret.reindex(intersection_date)
    dic = {}
    for date in intersection_date:
        data = 
    
    ls_ret=[pd.DataFrame(data=df_retfilter.ix[i].reindex(benchmark.ix[i].dropna().index.values)).rename(columns={i:'ret'}).assign(date=i) for i in ls_union_date]
    df_ret_pre=pd.concat(ls_ret,axis=0).reset_index()
    return df_ret_pre 


# <codecell>

