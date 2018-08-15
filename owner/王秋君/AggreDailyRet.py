# <codecell>

import pandas as pd
import numpy as np

def AggreDailyRet(context,DailyRetAttri,startDate,endDate):
    if endDate< min(list(DailyRetAttri['DailyRetAttribution'].index)) or startDate> max(list(DailyRetAttri['DailyRetAttribution'].index)):
        raise Exception("the daterange you need didn't match the dailyretattri daterange")
    
    DailyRet=DailyRetAttri['DailyRetAttribution']
    DailyRet_slice=DailyRet[(DailyRet.index <= endDate) & (DailyRet.index >= startDate)].sort_index()
    DailyPortVal=DailyRetAttri['PortVal']
    
    if 'date' in DailyPortVal.columns:
        datecol='date'
    datecol='shiftdate'
    base_date_portval=float(DailyPortVal[DailyPortVal[datecol] ==startDate]['PortVal'])
    
    df_daterange_aggret=pd.DataFrame(data=DailyRet_slice.sum(axis=0)/base_date_portval,columns=['aggret']).reset_index()
    return df_daterange_aggret
