# <codecell>

import pandas as pd
from lib.gftTools import gftIO
from lib.gftTools import gsUtils
import numpy as np
from numpy import NaN
import warnings
warnings.filterwarnings("ignore")

def BrinsonAttribution(context,start_date,end_date,portfolio_wt,benchmark,close_price):
    '''
    parameter
    -----
    start_date: DateTimeIndex
    end_date: DateTimeIndex
    portfolio_wt: OOTV, portfolio weight with industry info,filling weight
    benchmark: OOTV, benchmark weight with industry info
    close_price：后复权收盘价,OTV
    
    '''
    if start_date >= end_date:
        raise ValueError('startdate should be earlier than enddate!')
    df_l_benchmark = benchmark.asColumnTab()
    df_l_portfolio_wt = portfolio_wt.asColumnTab()
    df_close_price = close_price.asMatrix()
    #rename
    df_l_portfolio_wt.columns = ['date','symbol','weight','ind']
    df_l_benchmark.columns = ['date','symbol','weight','ind']

    '''data preparation '''
    #prepare for slicing dates
    df_l_portfolio_wt = df_l_portfolio_wt.dropna(subset=['weight'])
    df_l_portfolio_wt = df_l_portfolio_wt[df_l_portfolio_wt['weight']!=0]
    df_l_benchmark = df_l_benchmark.dropna(subset=['weight'])
    df_close_price = df_close_price.dropna(axis = 1, how = 'all')
    
    businessdays = df_close_price.index
    if (min(businessdays) > end_date) | (max(businessdays) <start_date):
        raise ValueError ('dates should be reset')
    end = max(businessdays[businessdays<=end_date])

    #prepare for slicing symbols
    portfolioSymbols = df_l_portfolio_wt['symbol'].unique()
    benchmarkSymbols = df_l_benchmark['symbol'].unique()
    allSymbols = np.unique(np.union1d(portfolioSymbols, benchmarkSymbols))
    cashSymbol = gsUtils.getCashGid()[0]

    #drop cash in portfolio_wt
    df_l_portfolio_wt = df_l_portfolio_wt[df_l_portfolio_wt['symbol']!=cashSymbol]
    df_l_portfolio_wt = df_l_portfolio_wt.sort_values('date')

    #slice dates
    start_date = gsUtils.alignDate(start_date, businessdays)
    begin = max(start_date,min(df_l_portfolio_wt['date']))
    df_l_portfolio_wt = df_l_portfolio_wt[(df_l_portfolio_wt['date']>= begin) & (df_l_portfolio_wt['date']<=end)]
    alldates = pd.to_datetime(df_l_portfolio_wt['date'].unique())  
    alldates_benchmark = pd.to_datetime(df_l_benchmark['date'].unique())
    #if benchmark dates missing, find common dates between portfolio and benchmark   
    if len(np.setdiff1d(alldates, alldates_benchmark)) > 0:
        df_l_portfolio_wt = df_l_portfolio_wt[df_l_portfolio_wt['date'].isin(alldates_benchmark)]
    df_l_benchmark = df_l_benchmark[(df_l_benchmark['date']>=begin) & (df_l_benchmark['date']<=end)]
    df_l_benchmark = df_l_benchmark.sort_values('date')
    #slice dates for closeprice
    priceDates = pd.to_datetime(df_l_benchmark['date'].unique())
    if not(end_date in priceDates):
        priceDates = priceDates.append(pd.Index([end])) #add end_date if not included
    priceDates = priceDates.sort_values()

    #calculate return
    df_close_price = df_close_price.reindex(priceDates, allSymbols, fill_value=NaN)   
    df_tot_return_index = df_close_price.pct_change(1).shift(-1).fillna(0.0)
    df_l_tot_return_index = gftIO.convertMatrix2ColumnTab(df_tot_return_index)
    df_l_tot_return_index.columns = ['date', 'symbol', 'return']
    df_l_tot_return_index = df_l_tot_return_index.sort_values('date')


    #calculate industry weight&industry return
    df_l_portwgt= df_l_portfolio_wt.groupby(['ind','date'], as_index=False).sum()  #industry weight
    df_l_portwgt = df_l_portwgt.sort_values('date')
    df_l_benchmark_wgt = df_l_benchmark.groupby(['ind', 'date'], as_index= False).sum() #industry weight
    df_l_benchmark_wgt = df_l_benchmark_wgt.sort_values('date')

    df_l_portfolio_wt = pd.merge(df_l_portfolio_wt,df_l_portwgt,how='left',on=['ind','date'],suffixes = ('', '_ind')) #get industry weight
    df_l_benchmark= pd.merge(df_l_benchmark,df_l_benchmark_wgt,how='left',on=['ind','date'],suffixes = ('', '_ind')) #get industry weight

    df_l_portfolio_wt['weight_ind_pct'] = df_l_portfolio_wt['weight']/df_l_portfolio_wt['weight_ind']  #stock weight/industry weight
    df_l_benchmark['weight_ind_pct'] = df_l_benchmark['weight']/df_l_benchmark['weight_ind']

    df_l_portfolio_wt = pd.merge(df_l_portfolio_wt,df_l_tot_return_index, how = 'left', on = ['symbol', 'date'], sort=False)
    df_l_benchmark = pd.merge(df_l_benchmark,df_l_tot_return_index, how = 'left', on = ['symbol', 'date'], sort=False) 

    df_l_portfolio_wt['return_pcg'] = df_l_portfolio_wt['weight_ind_pct']*df_l_portfolio_wt['return']  #calculate w*r
    df_l_benchmark['return_pcg'] = df_l_benchmark['weight_ind_pct']*df_l_benchmark['return']

    df_l_portret = df_l_portfolio_wt.groupby(['ind','date'],as_index= False)['return_pcg'].sum()  #get industry return
    df_l_benchret = df_l_benchmark.groupby(['ind','date'],as_index= False)['return_pcg'].sum()
    df_l_portret = df_l_portret.sort_values('date')
    df_l_benchret = df_l_benchret.sort_values('date')

    #Prepare for Q1,Q2,Q3,Q4( Q1:基准组合 Q2：积极资产配置组合 Q3.积极股票选择组合 Q4.实际组合 )
    Q1 =  pd.merge(df_l_benchmark_wgt,df_l_benchret, how = 'left', on = ['ind', 'date'])
    Q2 =  pd.merge(df_l_portwgt,df_l_benchret, how = 'left', on = ['ind', 'date'])
    Q3 =  pd.merge(df_l_benchmark_wgt,df_l_portret, how = 'left', on = ['ind', 'date'])
    Q4 =  pd.merge(df_l_portwgt,df_l_portret, how = 'left', on = ['ind', 'date'])

    #calculate cumulative return, p,aa,ss,b分别是基金实际组合、积极资产配置组合、积极股票选择组合以及基准组合的k期复合收益率
    Q1['b'] = Q1['weight'].mul(Q1['return_pcg'], axis=0)
    Q2['aa'] = Q2['weight'].mul(Q2['return_pcg'], axis=0)
    Q3['ss'] = Q3['weight'].mul(Q3['return_pcg'], axis=0)
    Q4['p'] = Q4['weight'].mul(Q4['return_pcg'], axis=0)

    b = Q1.groupby(['date'])['b'].sum()
    aa = Q2.groupby(['date'])['aa'].sum()
    ss = Q3.groupby(['date'])['ss'].sum()
    p= Q4.groupby(['date'])['p'].sum()

    b = np.cumprod(1+b)-1
    aa  = np.cumprod(1+aa)-1
    ss = np.cumprod(1+ss)-1
    p  = np.cumprod(1+p)-1

    b = pd.Series.to_frame(b).fillna(0)
    aa = pd.Series.to_frame(aa).fillna(0)
    ss = pd.Series.to_frame(ss).fillna(0)
    p = pd.Series.to_frame(p).fillna(0)

    Q1 =  pd.merge(Q1,b, how = 'left', left_on = ['date'],right_index = True)
    Q2 =  pd.merge(Q2,aa, how = 'left',left_on = ['date'],right_index = True)
    Q3 =  pd.merge(Q3,ss, how = 'left',left_on = ['date'],right_index = True)
    Q4 =  pd.merge(Q4,p, how = 'left', left_on = ['date'],right_index = True)

    Q1['b_y'] = Q1.groupby(['ind'])['b_y'].apply(lambda x: x.shift(1)).fillna(0)
    Q2['aa_y'] = Q2.groupby(['ind'])['aa_y'].apply(lambda x: x.shift(1)).fillna(0)
    Q3['ss_y'] = Q3.groupby(['ind'])['ss_y'].apply(lambda x: x.shift(1)).fillna(0)
    Q4['p_y'] = Q4.groupby(['ind'])['p_y'].apply(lambda x: x.shift(1)).fillna(0)

    Q1['b']= Q1['weight']*Q1['return_pcg']*(Q1['b_y']+1)
    Q2['aa']= Q2['weight']*Q2['return_pcg']*(Q2['aa_y']+1)
    Q3['ss']= Q3['weight']*Q3['return_pcg']*(Q3['ss_y']+1)
    Q4['p']= Q4['weight']*Q4['return_pcg']*(Q4['p_y']+1)

    q1 = Q1[['ind','date','b']]
    q2 = Q2[['ind','date','aa']]
    q3 = Q3[['ind','date','ss']]
    q4 = Q4[['ind','date','p']]

    summary0 = pd.merge(q1,q2,how = 'left',on = ['ind','date'])
    summary1 = pd.merge(summary0,q3,how = 'left',on = ['ind','date'])
    summary2 = pd.merge(summary1,q4,how = 'left',on = ['ind','date'])
    summary= summary2.copy()
    summary.fillna(0,inplace=True)
    summary['AR'] = summary['aa']-summary['b']  #Pure Sector Allocation
    summary['SR'] = summary['ss']-summary['b']  #Within-Sector selection return
    summary['IR'] = summary['p']-summary['ss']-summary['aa']+summary['b']
    summary['TotalValueAdded'] = summary['AR']+summary['SR']+summary['IR']
    summary = pd.merge(df_l_benchmark_wgt,summary,how='outer',on = ['ind','date'])
    summary = pd.merge(summary,df_l_portwgt,how = 'outer',on = ['ind','date'])
    summary.fillna(0,inplace=True)
    summary.columns=['ind','date','bmweight','cumulativeBenRet','portreturncontribution',
                     'bmreturncontribution','cumulativePortRet','AssetAllocation','StockSelection','Interaction','TotalValueAdded','portweight']
    result = summary
    result = result[['ind','date','portweight','bmweight','portreturncontribution',
                       'bmreturncontribution','cumulativePortRet','cumulativeBenRet','AssetAllocation','StockSelection','Interaction','TotalValueAdded']]
    portfolio_length = len(df_l_portwgt['date'].unique())
    benchmark_length = len(df_l_benchmark_wgt['date'].unique())
    final_result = {'result':result,'portfolio_length':portfolio_length,'benchmark_length':benchmark_length}
    return final_result
