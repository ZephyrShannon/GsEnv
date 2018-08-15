# <codecell>

import numpy as np
import pandas as pd
from sklearn import linear_model
from lib.gftTools import gftIO
from functools import reduce     
import datetime  


# x0: date, returns, symbol
# create_newx: dictionary of dataframes
# stock_listdate: variable, date, value (dates of trading classified as 1, else is NaN)


def SliceXYData(context,x0,datepoint,period,create_newx,stock_listdate):
    ##step1:prepare return data
    df_return_data=x0.asColumnTab()
    ls_date=np.sort(np.unique(list(df_return_data.date)))
    if period <0:
        try:
            ls_need_date = ls_date[ls_date < datepoint][period:]
        except:
            raise Exception("more data needed")
    else:
        try:
            ls_need_date = ls_date[ls_date > datepoint][:period]
        except:
            raise Exception("more data needed")
            
    ls_newcolraw=list(map(lambda x:'x'+str(x),list(range(0,25))))##自变量是25个
    ##观察点取24个月，每个月的自变量是历史25个月每月的月收益率
    ls_newcol=ls_newcolraw+['y']
    
    ##股票的上市日期进行数据清洗
    df_listdate=stock_listdate.asColumnTab().dropna(subset=['value'])
    
    dict_return_xy_final ={date:DailyDataPre(date,df_return_data,ls_date,ls_newcol,df_listdate) for date in ls_need_date}
    ##ls_need_date is 24 months snapshot,also is the factor exposure date
    
    
    ###step2:create new x
    
    dict_x={create_newx[i][0]:create_newx[i][1].asMatrix() for i in range(len(create_newx))}   
#    dict_datelength={i:len(j.index) for i,j in dict_x.items()}
#    float_quantile=np.percentile(a=(list(dict_datelength.values())),q=5)
#    dict_x={k: v for k, v in dict_x.items() if len(v.index) >= float_quantile}
    ls_allfactor_name=list(dict_x.keys())
    ls_x_date=[list(i.index) for i in dict_x.values()]
    ls_alldates_x=reduce(np.intersect1d,ls_x_date) 
    ls_newx_date = [i for i in ls_need_date if i not in ls_alldates_x]
    if len(ls_newx_date) != 0:
        raise Exception('date not enough')
    dict_symbol={date:dict_return_xy_final[date]['symbol'].values for date in ls_need_date}
    dict_newx={date:x_merge(dict_x,date,ls_allfactor_name,dict_symbol) for date in ls_need_date}
    
    ls_final_xy = [dict_return_xy_final[date].merge(dict_newx[date],on=['symbol']).assign(date=date) for date in ls_need_date]
    df_final_xy = pd.concat(ls_final_xy,axis=0)
    return df_final_xy
    
def x_merge(dict_x,date,ls_allfactor_name,dict_symbol):
    ls_raw_df_x=[dict_x[i].reindex(index=[date],columns=dict_symbol[date]).rename(index={date:i}) for i in ls_allfactor_name] 
    df_x_onedate=pd.concat(ls_raw_df_x,axis=0).T
                          
    df_x_onedate.columns=list(map(lambda x:'x'+str(x),list(range(25,25+df_x_onedate.shape[1]))))                      
    #df_x_onedate.fillna(df_x_onedate.mean(),inplace=True)
    df_x_onedate_final=df_x_onedate.reset_index().rename(columns={'index':'symbol'})
    return df_x_onedate_final

def DailyDataPre(i,df_return_data,ls_date,ls_newcol,df_listdate):
    df_return_new=df_return_data.set_index('symbol')
    newi=ls_date[ls_date >i][0]
    ls_xy_date = ls_date[ls_date <=newi][-26:]
        
    ls_symbol_need=df_return_new[df_return_new.date == i].index.values
    ls_return_xy=[df_return_new[df_return_new.date == j][['ret']].reindex(ls_symbol_need).rename(columns={'ret':j}) for j in ls_xy_date]
    df_return_xy=pd.concat(ls_return_xy,axis=1)
    #newcol_len=len(df_return_xy.columns)
    #df_return_xy.columns=ls_newcol[]  ##x0是距离当前观察点最远的那个日期
    
    ###剔除上市不满一年的股票
    listdate = i -datetime.timedelta(days=365)
    ls_delsymbol = df_listdate[df_listdate.idname > listdate].variable     
    
    ls_fnl_symbol =[i for i in list(df_return_xy.index.values) if i not in list(ls_delsymbol)]
    df_return_xy_fnl=df_return_xy.reindex(index=ls_fnl_symbol)
    
    df_return_xy_fnl.fillna(0,inplace=True)###缺失的原因是当前股票还没有上市
    df_return_xy_fnl_new=df_return_xy_fnl.reset_index()
    return df_return_xy_fnl_new
