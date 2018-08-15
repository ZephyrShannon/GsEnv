# <codecell>

import numpy as np
import pandas as pd

def StrategyCreatePrice(strategyWgt,strategyDict):
    df_strategyWgt = strategyWgt.asMatrix()
    allStrategies = df_strategyWgt.columns
    allDates = df_strategyWgt.index
    n = len(allDates)
    for i in allStrategies:
        if not i in strategyDict.keys():
            raise Exception("missing strategy in the dict")
        df_cumret = strategyDict[i].cumret.asMatrix()    
        allDates = np.intersect1d(allDates, df_cumret.index)       
        if len(allDates) < 1:
            raise Exception("no common dates for holding and strategyWgt")
            
    result = pd.DataFrame(0., index = allDates, columns = allStrategies)
    for i in allStrategies:
        df_cumret = strategyDict[i].cumret.asMatrix()
        result.loc[allDates, i] = df_cumret.loc[allDates, df_cumret.columns[0]]
    result = result + 1   
    result = result.dropna(axis=0, how="all")
    return result
