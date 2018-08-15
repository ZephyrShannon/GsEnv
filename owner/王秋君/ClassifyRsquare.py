# <codecell>

from lib.gftTools import gftIO
import numpy as np
import pandas as pd

def ClassifyRsquare(context,y,yhat):

    y=y.asColumnTab()
    yhat=yhat.asColumnTab()
    
    ytName = None
    yvName = None
    for colName in y.columns:
        if gftIO.istimestamparray(np.array(y[colName])):
            if ytName is None:
                ytName = colName
        if (y[colName].dtype == np.float64 or y[colName].dtype == np.int64):
            if yvName is None:
                yvName = colName
                
    yhattName = None
    yhatvName = None
    
    for colName in yhat.columns:
        if gftIO.istimestamparray(np.array(yhat[colName])):
            if yhattName is None:
                yhattName = colName
        if (yhat[colName].dtype == np.float64 or yhat[colName].dtype == np.int64):
            if yhatvName is None:
                yhatvName = colName
                
    df_y=y.sort_values(ytName,ascending=True)
    df_yhat=yhat.sort_values(yhattName,ascending=True)
    
    df_y_yhat = pd.merge_asof(df_yhat,
                              df_y, left_on =yhattName,right_on =ytName,allow_exact_matches=False)   
    
    df_y_yhat.dropna(subset=[ytName],how='any',inplace=True)
    y_mean=df_y_yhat[yvName].mean()
    
    rsquare=((df_y_yhat[yhatvName]-y_mean)**2).sum()/((df_y_yhat[yvName]-y_mean)**2).sum()
    
    return rsquare

# <codecell>



# <codecell>


