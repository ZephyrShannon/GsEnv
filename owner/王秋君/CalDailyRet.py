# <codecell>

from lib.gftTools import gftIO
import numpy as np
import pandas as pd
from functools import reduce


'''
stock_price=x0
stock_wgt=x1
riskmodel=x2
'''

class Riskmodel(object):
    
    def __init__(self,data,dt_selecteddate,allsymbol):
        self.data=data
        self.selectedate=dt_selecteddate
        self.allsymbol=allsymbol
        
    def getfactorlist(self,i):
        return (self.data[gftIO.gidInt2Str(self.data['osets'].asColumnTab().ix[i,0])].asColumnTab()['O0']).apply(lambda x:gftIO.gidInt2Str(x)).tolist()
    
    def factorcnt(self):
        return len(self.data['osets'].asColumnTab())
    
    def getallFactor(self):
        allfactor=[]
        for i in range(self.factorcnt()):
            allfactor.extend(self.getfactorlist(i))
        return allfactor
    
    def selectData(self):
        dict_fexpo=dict([(factorname,self.data[factorname].asMatrix().reindex(columns=self.allsymbol)) for factorname in self.getallFactor()])
        return dict_fexpo
    
    def Fexpomerge(self):
        dt_latest = self.selectedate 
        ls_raw_df_fexpo=[self.selectData()[factorname].reindex(index=[dt_latest]).rename(index={dt_latest:factorname}) for factorname in self.getallFactor()] 
        df_fexpo_onedate=pd.concat(ls_raw_df_fexpo,axis=0).fillna(0)
        df_fexpo_onedate.index=list(gftIO.strSet2Np(np.array(df_fexpo_onedate.index)))
        return df_fexpo_onedate.T

def CalDailyRet(context,stock_price,stock_wgt,riskmodel,incind):
    ##step1:wgt preprocess
    df_wgt=stock_wgt.asMatrix()
    ls_date_wgt_raw=sorted(list((list(df_wgt.index))))
    if 'idname' in df_wgt.columns:
        df_wgt=df_wgt.drop(['idname'],axis=1)
    
    ls_aname=list(list(df_wgt.columns))       
    
    ##step2:factor expo preprocess
    ls_fexponame=list(map(gftIO.gidInt2Str,list(riskmodel['osets'].asColumnTab()['O0'])))
    sty_factor_name=sorted(list(map(gftIO.gidInt2Str,list(riskmodel[ls_fexponame[1]].asColumnTab()['O0']))))
    
    if incind == 1:
        ind_factor_name=sorted(list(map(gftIO.gidInt2Str,list(riskmodel[ls_fexponame[0]].asColumnTab()['O0']))))
        allfactor =ind_factor_name +sty_factor_name
    else:
        allfactor=sty_factor_name
    
    ##calculate factor exposure date
    dict_risk_expo_new = {factorname: riskmodel[factorname].asMatrix().dropna(how='all') for factorname in list(allfactor)}
    ls_ls_fexpodate=list([dict_risk_expo_new[factorname].index.tolist() for factorname in dict_risk_expo_new.keys()]) 
    ls_alldates_fexpo=reduce(np.intersect1d,ls_ls_fexpodate)    
    
    ##step3:factor return preprocess
    dict_factor_map={i+'.ret':i for i in allfactor}
    ls_ls_dates_facret=[list(v.index) for k, v in riskmodel.items() if k in list(dict_factor_map.keys())]
    ls_facret_dates=reduce(np.intersect1d,ls_ls_dates_facret)
    
    ##step4:stock price preprocess
    df_stock_price=stock_price.asMatrix()
    if 'idname' in df_stock_price.columns:
        df_stock_price=df_stock_price.drop(['idname'],axis=1)
    df_stock_price=df_stock_price.reindex(columns=ls_aname)
    df_stock_ret = df_stock_price / df_stock_price.shift(1)-1
    ls_stockret_dates=list(df_stock_ret.index)[1:]                                                  
    
    ###wgt shift date
    
    '''
    get monthly weight
    
    aa=df_wgt.copy()
    aa['date']=aa.index
    aa['ym']=aa['date'].apply(lambda x:x.year*100+x.month)
    aa=aa.drop_duplicates(subset=['ym'],keep='last')
    aa.drop(['date','ym'],axis=1,inplace=True)
    df_wgt=aa.iloc[:-1,]
    '''
    
    ###if it is monthly strategy,the align the stock weight
    ls_date_wgt=sorted(list(filter(lambda x:(x <= max(ls_date_wgt_raw)) & (x >= min(ls_date_wgt_raw)),ls_stockret_dates)))
    
    ls_check=[i for i in ls_date_wgt if i not in ls_date_wgt_raw]
    if len(ls_check) != 0:
        ##stock ret process
        df_ret_align=df_stock_ret.reindex(ls_check)
        df_ret_align['cash'] =0
        
        ##np.nan  change to 0
        df_ret_align.fillna(0,inplace=True)
        
        df_ret_align=df_ret_align+1
        #df_ret_align=df_ret_align.reindex(ls_date_wgt,fill_value=1).sort_index()
        
        ##stock wgt process
        df_wgt_align=df_wgt.copy()
        df_wgt_align.fillna(0,inplace=True)
        df_wgt_align['cash']=1 -df_wgt_align.sum(axis=1)

        #df_wgt_align=df_wgt.reindex(index=ls_date_wgt,fill_value=1)
        ###stock wgt * stock ret
        df_ret_wgt=df_ret_align.append(df_wgt_align).sort_index()
        
        ##get align date
        df_dateMap = pd.DataFrame({'targetDate':ls_date_wgt_raw, 'idx':np.arange(len(ls_date_wgt_raw))}, index=ls_date_wgt_raw)
        df_dateMap = df_dateMap.reindex([ls_date_wgt], method='ffill')
        
        ##merge two table
        df_ret_wgtall =df_ret_wgt.merge(df_dateMap,left_index=True,right_index=True)
        df_ret_wgtall.drop(['targetDate'],axis=1,inplace=True)
        df_ret_wgtfnl = df_ret_wgtall.groupby('idx').apply(lambda x:x.cumprod(axis=0)).drop(['idx'],axis=1)

        ##standardize wgt
        df_date_wgtall =1 / df_ret_wgtfnl.sum(axis=1)
        df_ret_std = df_ret_wgtfnl.multiply(df_date_wgtall,axis='index') 
        df_wgt=df_ret_std.drop(['cash'],axis=1)
    else:
        ls_date_wgt=ls_date_wgt_raw  
        
    
    ##step5:calculate daily portfolio value:
    df_wgt_raw=df_wgt.copy()
    
    df_wgt['date']=df_wgt.index
    df_wgt['shiftdate']=df_wgt['date'].shift(-1)
    df_wgt.index=df_wgt['shiftdate']                      
    df_wgt.drop(['date','shiftdate'],axis=1,inplace=True)
    
    df_stock_ret=df_stock_ret.reindex(index=list(df_wgt.index))
    df_portvalue=1+((df_wgt * df_stock_ret).sum(axis=1))
    df_portfnlvalue=df_portvalue.cumprod(axis=0)
    
    ##step6:calculate xp * factorreturn
    ls_date_range=list(set(ls_alldates_fexpo).intersection(set(ls_date_wgt)).intersection(set(ls_facret_dates)).intersection(set(list(df_portfnlvalue.index))))
    
    ##factor return/wgt
    dict_facret={dict_factor_map[k]: v.reindex(index=ls_date_range) for k, v in riskmodel.items() if k in list(dict_factor_map.keys())}
    df_wgt_raw=df_wgt_raw.reindex(index=ls_date_range)
    ##xp * factor return
    ls_df_fexpo=[fexpoprocess(k,v,ls_date_range,ls_aname,df_wgt_raw,dict_facret) for k, v in dict_risk_expo_new.items()]
    
    df_expo=pd.concat(ls_df_fexpo,axis=1)  
    df_portfnlvalue=df_portfnlvalue.reindex(index=ls_date_range)      

    df_final_return=df_expo.multiply(df_portfnlvalue,axis='index')        
        
    return df_final_return
    
def fexpoprocess(k,v,ls_date_range,ls_aname,df_wgt_raw,dict_facret):
    v=v.reindex(index=ls_date_range,columns=ls_aname)
    v1=v * df_wgt_raw 
    v2=pd.DataFrame(data=v1.sum(axis=1),columns=[dict_facret[k].columns[0]])
    v3 = v2 * dict_facret[k]
    return v3

# <codecell>



# <codecell>



# <codecell>


