# <codecell>

from lib.gftTools import gftIO
import numpy as np
import pandas as pd
from lib.gftTools import gsUtils

'''
stockPrice=x0
stockWgt=x1
'''

def AlignWgt(context,stockPrice,stockWgt):
    df_wgt=stockWgt.asMatrix()
    ls_date_wgt_raw=sorted(list((list(df_wgt.index))))
    if 'idname' in df_wgt.columns:
        df_wgt=df_wgt.drop(['idname'],axis=1)
    ls_aname=list(list(df_wgt.columns)) 
    
    df_stock_price=stockPrice.asMatrix()
    if 'idname' in df_stock_price.columns:
        df_stock_price=df_stock_price.drop(['idname'],axis=1)
    df_stock_price=df_stock_price.reindex(columns=ls_aname)
    df_stock_ret = df_stock_price / df_stock_price.shift(1)-1
    ls_stockret_dates=list(df_stock_ret.index)[1:] 
    
    ls_date_wgt=sorted(list(filter(lambda x:(x <= max(ls_date_wgt_raw)) & (x >= min(ls_date_wgt_raw)),ls_stockret_dates)))
    ##check whether to align the stock weight
    ls_check=[i for i in ls_date_wgt if i not in ls_date_wgt_raw]
    if len(ls_check) != 0:
        ls_dateall=sorted(list(filter(lambda x: x >= min(ls_date_wgt_raw),ls_stockret_dates)))
        ls_dateall_cal=[i for i in ls_dateall if i not in ls_date_wgt_raw]       
        
        ##stock ret process
        df_ret_align=df_stock_ret.reindex(index=ls_dateall_cal)
        df_ret_align['cash'] =0
        ##np.nan  change to 0
        df_ret_align.fillna(0,inplace=True)
        df_ret_align=df_ret_align+1
        
        ##stock wgt process
        df_wgt_align=df_wgt.copy()
        df_wgt_align.fillna(0,inplace=True)
        cashSymbol=gsUtils.getCashGid()[0]
        if cashSymbol in df_wgt_align.columns:
            df_wgt_align['cash']=df_wgt_align[cashSymbol]
            df_wgt_align.drop([cashSymbol],axis=1,inplace=True)
            
        else:
            df_wgt_align['cash']=1 -df_wgt_align.sum(axis=1)

        ###stock wgt append stock ret
        df_ret_wgt=df_ret_align.append(df_wgt_align).sort_index()
        
        ##get align date
        df_dateMap = pd.DataFrame({'targetDate':ls_date_wgt_raw, 'idx':np.arange(len(ls_date_wgt_raw))}, index=ls_date_wgt_raw)
        df_dateMap = df_dateMap.reindex([ls_dateall], method='ffill')
        
        ##merge two table
        df_ret_wgtall =df_ret_wgt.merge(df_dateMap,left_index=True,right_index=True)
        df_ret_wgtall.drop(['targetDate'],axis=1,inplace=True)
        df_ret_wgtfnl = df_ret_wgtall.groupby('idx').apply(lambda x:x.cumprod(axis=0)).drop(['idx'],axis=1)

        ##standardize wgt
        df_date_wgtall =1 / df_ret_wgtfnl.sum(axis=1)
        df_ret_std = df_ret_wgtfnl.multiply(df_date_wgtall,axis='index') 
        df_wgt=df_ret_std.drop(['cash'],axis=1)
    
    return df_wgt

# <codecell>


