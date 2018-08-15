# <codecell>

import numpy as np
import pandas as pd

def StrategyCreateStockWgt(strategyWgt, strategyDict):
    df_strategyWgt = strategyWgt.asMatrix()
    allStrategies = df_strategyWgt.columns
    allDates = df_strategyWgt.index
    n = len(allDates)
    allSymbols = []
    for i in allStrategies:
        if not i in strategyDict.keys():
            raise Exception("missing strategy in the dict")
        df_holding = strategyDict[i].holding.asMatrix()
        allDates = np.intersect1d(allDates, df_holding.index)
        allSymbols = np.union1d(allSymbols, df_holding.columns)        
        if len(allDates) < 1:
            raise Exception("no common dates for holding and strategyWgt")
    result = pd.DataFrame(0., index = allDates, columns = allSymbols)
    for i in allStrategies:
        df_holding = strategyDict[i].holding.asMatrix()
        df_holding = df_holding.reindex(index=allDates, columns=allSymbols, fill_value=0)
        df_holding = df_holding.fillna(0)
        df_wgt = np.tile(df_strategyWgt.loc[allDates, [i]],len(allSymbols))
        df_wgt = np.nan_to_num(df_wgt)
        result = result + df_holding *df_wgt    
    result = result.replace(0, np.nan)
    result = result.dropna(axis=[0,1], how='all')
    return result
