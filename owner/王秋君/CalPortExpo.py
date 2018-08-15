# <codecell>

import pandas as pd
import numpy as np
from lib.gftTools import gftIO

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
    
def CalPortExpo(context,fexpo,wgt):
    
    df_wgt=wgt.asMatrix()
    ls_date_wgt=sorted(list((list(df_wgt.index))))
    if 'idname' in df_wgt.columns:
        df_wgt=df_wgt.drop(['idname'],axis=1)
    ls_aname=list(list(df_wgt.columns))
    
    ls_fexponame=list(map(gftIO.gidInt2Str,list(fexpo['osets'].asColumnTab()['O0'])))
    sty_factor_name=sorted(list(map(gftIO.gidInt2Str,list(fexpo[ls_fexponame[1]].asColumnTab()['O0']))))
    ind_factor_name=sorted(list(map(gftIO.gidInt2Str,list(fexpo[ls_fexponame[0]].asColumnTab()['O0']))))
    allfactor =ind_factor_name +sty_factor_name
    
    ##calculate factor exposure date
    dict_risk_expo_new = {factorname: fexpo[factorname].asMatrix().dropna(how='all') for factorname in list(allfactor)}
    ls_df_fexpo=[fexpoprocess(k,v,ls_date_wgt,ls_aname,df_wgt) for k, v in dict_risk_expo_new.items()]
    df_expo=pd.concat(ls_df_fexpo,axis=1)
    df_expo.columns=list(gftIO.strSet2Np(np.array(df_expo.columns)))                
    return df_expo
    
    
def fexpoprocess(k,v,ls_date_wgt,ls_aname,df_wgt):
    v=v.reindex(index=ls_date_wgt,columns=ls_aname)
    v1=v * df_wgt
    v2=pd.DataFrame(data=v1.sum(axis=1),columns=[k])
    return v2   

# <codecell>



# <codecell>



# <codecell>



# <codecell>


