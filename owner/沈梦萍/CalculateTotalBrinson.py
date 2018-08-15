# <codecell>

import numpy as np
import pandas as pd

def CalculatePeriodAttribution(context,brinson):
    '''
    Parameter
    ----
    brinson_daily:
    daily/lower frequency brinson Attribution result from brinson attribution
    dicts: keys include result,portfolio_length,benchmark_length
    
    '''
    total_result = brinson_daily['result'].groupby(['ind']).sum().reset_index()
    total_result['portweight']=total_result['portweight']/brinson_daily['portfolio_length']
    total_result['bmweight']=total_result['bmweight']/brinson_daily['benchmark_length']
    return total_result
