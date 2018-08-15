# <codecell>

import numpy as np
import pandas as pd

def PortfolioOptimize(target_mode,group_weight_min,position_limit,target_risk,expected_return,covariance_matrix):
    raise Exception("To be implemented")

# <codecell>

import numpy as np
import pandas as pd

from lib.gftTools import gftIO

# <codecell>

x0 = gftIO.zload("/home/jovyan/.gft/data/x0.pkl")
x1 = gftIO.zload("/home/jovyan/.gft/data/x1.pkl")
x2 = gftIO.zload("/home/jovyan/.gft/data/x2.pkl")
x3 = gftIO.zload("/home/jovyan/.gft/data/x3.pkl")
x4 = gftIO.zload("/home/jovyan/.gft/data/x4.pkl")
x5 = gftIO.zload("/home/jovyan/.gft/data/x5.pkl")
x6 = gftIO.zload("/home/jovyan/.gft/data/x6.pkl")
x6 = gftIO.transformDict4Name(x6)

# <codecell>

x6

# <codecell>

x6['g1'].asColumnTab()

# <codecell>

x6['gw1'].asColumnTab()

# <codecell>


