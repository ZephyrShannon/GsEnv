# <codecell>

import numpy as np
import pandas as pd

def Mad(x,maxValue,keepOrder,date):    
    raw_return=x[x['idname'] == date].rename(columns={'idname':'date'}).reset_index().drop('index',axis=1)
    x=x[x['idname'] == date]
    ls_x_var=list(x.variable)
    x.dropna(inplace=True)##remove missing values
    x=x.set_index('variable').drop('idname',axis=1)
    x=x['value']    
    
    if len(x) >1:
        medianvalue=x.median()
        madvalue=x.mad()*1.4826
        result=x - medianvalue
        if keepOrder == 1:            
            max_x=result[result > maxValue*madvalue]
            if len(max_x) >0:
                replace_max_x=madvalue * maxValue * (1 + max_x.rank(ascending=True,method='average')/len(max_x)/10000)
                result[result > maxValue*madvalue] = replace_max_x
            
            min_x=result[result < -maxValue*madvalue]
            if len(min_x) >0:
                replace_min_x=-madvalue * maxValue * (1 + (abs(min_x)).rank(ascending=True,method='average')/len(min_x)/10000)
                result[result < -maxValue*madvalue] = replace_min_x      
        else:
            absresult=abs(result)
            result=(np.sign(result)) * (absresult.where(absresult <= maxValue*madvalue,maxValue*madvalue))
        
        result  = result + medianvalue
        result=pd.DataFrame(result).reindex(ls_x_var).assign(date=date).reset_index()
        return result
    else:
        return raw_return

def WinsorizeMad(x,maxValue=5,keepOrder=0):
    x=x.asColumnTab()
    ls_date=np.unique(x.idname)
    
    ls_mad_result=[Mad(x,maxValue, keepOrder,date) for date in ls_date]
    result=pd.concat(ls_mad_result)
    return result
