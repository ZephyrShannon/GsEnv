# <codecell>

import numpy as np
import pandas as pd
from lib.gftTools import gsUtils
from lib.gftTools import gsConst

def StrategyAddPnlAndHolding(strategyList,cumretList,holdingList):
    result = {}
    if len(strategyList) != len(holdingList) or len(strategyList) != len(holdingList):
        raise Exception("strategyList, cumretList and holdingList have different length")
    for i in range(len(strategyList)):
        strategy = gsUtils.Strategy(strategyList[i][0], cumretList[i][1], holdingList[i][1])
        strategy.cumretGid = cumretList[i][0]
        strategy.holdingGid = holdingList[i][0]
        result[strategyList[i][0]] = strategy
    return result
